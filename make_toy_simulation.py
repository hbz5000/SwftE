from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import make_toy_demands
 
 
def initialize_simulation(start_year, current_year, environmental_flow_portion, initial_storage, cold_pool_storage, new_demands, enviro_demands, use_environmental_storage, use_class_2, user_groups, environmental_category, second_class_category, cold_pool_category):
  
  environmental_flow_budget = np.zeros(current_year - start_year + 1)
  if use_environmental_storage:
    environmental_storage_portion = environmental_flow_portion * 1.0
  else:    
    environmental_storage_portion = 0.0
  #initialize timeseries dictionaries
  total_storage = {}
  storage_categories = ['storage', 'storage_carryover', 'capacity', 'total_inflow']
  annual_categories = ['flood_release', 'total_release']
  for sc in storage_categories:
    total_storage[sc] = np.zeros(12*(current_year - start_year))
  for sc in annual_categories:
    total_storage[sc] = np.zeros(12*(current_year - start_year))
    total_storage[sc + '_annual'] = np.zeros(current_year - start_year)

  #initialize dictionaries for individual user gruops
  user_class = {}
  user_categories = ['total', 'storage_portion', 'class_1_portion', 'class_2_portion']
  ind_storage_categories = ['storage', 'storage_carryover']
  ind_annual_categories = ['missed', 'demand']
  for ug in user_groups:
    user_class[ug] = {}
    for uc in user_categories:
      user_class[ug][uc] = 0.0
    for st in ind_storage_categories:
      user_class[ug][st] = np.zeros(12*(current_year - start_year))
    for st in ind_annual_categories:
      #within environmental category, make sub-categories for different environmental types
      if ug == environmental_category:
        for demand_class in ['1', '2', '3', '4']:
          user_class[ug][st + '_class_' + demand_class] = np.zeros(current_year - start_year)
          user_class[ug][st + '_class_' + demand_class + '_annual'] = np.zeros(12*(current_year - start_year))
      else:
          user_class[ug][st] = np.zeros(current_year - start_year)
          user_class[ug][st + '_annual'] = np.zeros(12*(current_year - start_year))
      
    user_class[ug]['capacity'] = np.zeros(12*(current_year - start_year))

  #set user group demands
  for ug in user_groups:
    if ug == environmental_category:
      user_class[ug]['demands'] = {}
      for demand_class in ['1', '2', '3', '4']:
        user_class[ug]['demands'][demand_class] = enviro_demands['class' + demand_class]
    elif ug == cold_pool_category:
      user_class[ug]['demands'] = np.zeros((12, current_year - start_year + 1))      
    else:      
      user_class[ug]['demands'] = new_demands[ug]['monthly']
      
  for ug in user_groups:
    if ug != environmental_category:
      for x in range(0, 12):
        user_class[ug]['total'] += np.sum(user_class[ug]['demands'][x,:])

  #determine non-ewb portions
  non_environmental_use = 0.0
  class_1_non_env = 0.0
  class_2_non_env = 0.0
  for ug in user_groups:
    if ug != environmental_category:
      if ug in second_class_category:
        non_environmental_use += user_class[ug]['total']
        class_2_non_env += user_class[ug]['total']
      else:
        non_environmental_use += user_class[ug]['total']
        class_1_non_env += user_class[ug]['total']
      
  initial_storage_allocation = initial_storage - cold_pool_storage
  for ug in user_groups:
    #proportionally assign flow and storage to user groups based on total demand & the environmental portion
    if ug in second_class_category:
      if use_class_2:
        user_class[ug]['class_2_portion'] = (1.0 - environmental_flow_portion) * user_class[ug]['total'] / class_2_non_env
      else:      
        for portion_type in ['class_1_portion', 'class_2_portion']:
          user_class[ug][portion_type] = (1.0 - environmental_flow_portion) * user_class[ug]['total'] / non_environmental_use
        user_class[ug]['storage_portion'] = (1.0 - environmental_storage_portion) * user_class[ug]['total'] / non_environmental_use
        
    elif ug == environmental_category:
      for portion_type in ['class_1_portion', 'class_2_portion']:
        user_class[ug][portion_type] = environmental_flow_portion * 1.0
      user_class[ug]['storage_portion'] = environmental_storage_portion * 1.0
    else:
      if use_class_2:
        user_class[ug]['class_1_portion'] = (1.0 - environmental_flow_portion) * user_class[ug]['total'] / class_1_non_env
        user_class[ug]['storage_portion'] = (1.0 - environmental_storage_portion) * user_class[ug]['total'] / class_1_non_env
      else:
        for portion_type in ['class_1_portion', 'class_2_portion']:
          user_class[ug][portion_type] = (1.0 - environmental_flow_portion) * user_class[ug]['total'] / non_environmental_use
        user_class[ug]['storage_portion'] = (1.0 - environmental_storage_portion) * user_class[ug]['total'] / non_environmental_use

    #assign initial carry-over storage to each group
    if ug == cold_pool_category:
      user_class[ug]['storage'][0] = cold_pool_storage
    else:
      for storage_type in ['storage', 'storage_carryover']:
        if use_environmental_storage:
          user_class[ug][storage_type][0] = initial_storage_allocation * user_class[ug]['storage_portion']
        else:        
          if ug != environmental_category:
            user_class[ug][storage_type][0] = initial_storage_allocation * user_class[ug]['storage_portion'] /(1.0 - environmental_storage_portion)
      
  return total_storage, user_class

def get_total_inflow(values, start_year, current_year):
  total_inflow = np.zeros((12,current_year - start_year + 1))
  total_evap = np.zeros((12,current_year - start_year + 1))
  total_fci = np.zeros((12,current_year - start_year + 1))
  for index, row in values.iterrows():
    if index.month > 9:
      month_num = index.month - 10
      year_num = index.year - start_year + 1
    else:
      month_num = index.month + 2
      year_num = index.year - start_year
    total_inflow[month_num, year_num] += row['SHA_inf'] * 1.98/1000000.0
    total_evap[month_num, year_num] += row['SHA_evap'] * 1.98/1000000.0
    if index.day == 1:
      total_fci[month_num, year_num] = row['SHA_fci']
      
  return total_inflow, total_evap, total_fci

def find_seniority_cutoffs(user_groups, user_class, second_class_category, environmental_category):
  class_1_cutoff = 0.0
  class_2_total = 0.0
  for ug in user_groups:
    max_year = 0.0
    for y in range(0, 25):
      if ug != environmental_category:
        max_year += np.sum(user_class[ug]['demands'][:,y])/25.0
    if ug in second_class_category or ug == environmental_category:
      class_2_total += max_year
    else:
      class_1_cutoff += max_year
  return class_1_cutoff, class_2_total


def run_simulation(user_class, environmental_flow_portion, cold_pool_storage, off_site_storage_capacity, off_site_diversion_capacity, start_year, current_year, user_groups, tocs_rule, total_storage, total_inflow, total_evap, total_fci, class_1_cutoff, class_2_total, environmental_category, second_class_category, cold_pool_category, use_environmental_storage):
  datetime_index = []
  iteration_year = start_year - 1
  start_month = 10
  off_site_storage = 0.0
  max_off_site = 0.0
  environmental_flow_budget = np.zeros(current_year - start_year + 1)
  #start annual loop
  for x in range(0, current_year - start_year):
    annual_flow = 0.0
    for ug in user_groups:
      if ug != cold_pool_category and x > 0:
        #when the year turns over, move individual user storage to 'carryover' storage
        user_class[ug]['storage_carryover'][x*12] = user_class[ug]['storage'][x*12 - 1] * 1.0
    #start monthly loop
    for y in range(0,12):
      datetime_index.append(datetime(iteration_year, start_month, 1, 0 ,0))#create datetime index for results
      total_storage['total_inflow'][y + x*12] = total_inflow[y,x] - total_evap[y,x]#adjust daily storage for inflow & evap

      for ug in user_groups:
        #divide flow into user group storage pools
        if y + x*12 > 0:          
          if annual_flow < class_1_cutoff:
            user_class[ug]['storage'][y + x*12] = user_class[ug]['storage'][y + x*12 - 1] + (total_inflow[y,x] - total_evap[y,x])*user_class[ug]['class_1_portion'] 
          else:
            user_class[ug]['storage'][y + x*12] = user_class[ug]['storage'][y + x*12 - 1] + (total_inflow[y,x] - total_evap[y,x])*user_class[ug]['class_2_portion']
              
        #divide flows within the environmental category
        if ug == environmental_category:
          if use_environmental_storage:
            class_2_demand = 0.0
            #find remaining expected inflow (perfect information)
            expected_inflow = (np.sum(total_inflow[y:,x]) - np.sum(total_evap[y:,x]))*user_class[ug]['class_1_portion'] 
            #find remaining expected class 1/2 environmental demands
            class_1_demand = np.sum(user_class[ug]['demands']['1'][y:,x])
            class_2_demand = 0.0
            for demand_class in ['2', '3', '4']:
              class_2_demand += np.sum(user_class[ug]['demands'][demand_class][y:,x])
            for demand_class in ['1', '2', '3', '4']:
              #find class 1/2 allocations
              enviro_allocation = 0.0
              if demand_class == '1':
                if class_1_demand > 0.0:
                  enviro_allocation = min((expected_inflow + user_class[ug]['storage'][y + x*12]) / class_1_demand, 1.0)
              else:
                if class_2_demand > 0.0:
                  enviro_allocation = min(max(expected_inflow - class_1_demand + user_class[ug]['storage'][y + x*12], 0.0) / class_2_demand, 1.0)

              #calculate any missed demands b/c of lack of storage
              total_enviro_demands = user_class[ug]['demands'][demand_class][y,x] * enviro_allocation
              this_period_miss = max(total_enviro_demands - user_class[ug]['storage'][y + x*12], 0.0) + (1.0 - enviro_allocation) * user_class[ug]['demands'][demand_class][y,x]
              this_period_release = max(min(total_enviro_demands, user_class[ug]['storage'][y + x*12]), 0.0)
              total_storage['total_release'][y + x*12] += this_period_release
              total_off_site_release = min(off_site_storage, this_period_miss)
              this_period_miss -= total_off_site_release
              off_site_storage -= total_off_site_release
               
              #claculate storage change
              if (y + x*12) > 0:
                user_class[ug]['storage'][y + x*12] -= this_period_release
                if y > 0:
                  #keep track of carryover storage
                  user_class[ug]['storage_carryover'][y + x*12] = min(user_class[ug]['storage_carryover'][y + x*12 - 1], user_class[ug]['storage'][y + x*12])
                #record demand and demand shortfalls for each environmental class
                user_class[ug]['missed_class_' + demand_class][x] += this_period_miss
                user_class[ug]['demand_class_' + demand_class][x] += user_class[ug]['demands'][demand_class][y,x]
                user_class[ug]['demand_class_' + demand_class + '_annual'][y + x*12] += user_class[ug]['demands'][demand_class][y,x]
                user_class[ug]['missed_class_' + demand_class + '_annual'][y + x*12] += this_period_miss
          else:
            if (y + x*12) > 0:
              user_class[ug]['storage'][y + x*12] -= (total_inflow[y,x] - total_evap[y,x])*user_class[ug]['class_1_portion'] 
            total_enviro_inflow = (total_inflow[y,x] - total_evap[y,x])*user_class[ug]['class_1_portion']
            this_period_release = (total_inflow[y,x] - total_evap[y,x])*user_class[ug]['class_1_portion']
            total_storage['total_release'][y + x*12] += this_period_release
            #record demand and demand shortfalls for each environmental class
            for demand_class in ['1', '2', '3', '4']:
              this_period_miss = max(user_class[ug]['demands'][demand_class][y,x] - total_enviro_inflow, 0.0)
              total_enviro_inflow -= min(user_class[ug]['demands'][demand_class][y,x], total_enviro_inflow)
              if (y + x*12) > 0:
                user_class[ug]['missed_class_' + demand_class][x] += this_period_miss
                user_class[ug]['demand_class_' + demand_class][x] += user_class[ug]['demands'][demand_class][y,x]
                user_class[ug]['demand_class_' + demand_class + '_annual'][y + x*12] += user_class[ug]['demands'][demand_class][y,x]
                user_class[ug]['missed_class_' + demand_class + '_annual'][y + x*12] += this_period_miss
        else:
          #find demand and shortage for non-environmental groups
          this_period_miss = max(user_class[ug]['demands'][y,x] - user_class[ug]['storage'][y + x*12], 0.0)
          this_period_release = max(min(user_class[ug]['demands'][y,x], user_class[ug]['storage'][y + x*12]), 0.0)
          total_storage['total_release'][y + x*12] += this_period_release
          if (y + x*12) > 0:
            user_class[ug]['storage'][y + x*12] -= this_period_release
            user_class[ug]['missed'][x] += this_period_miss
            user_class[ug]['demand'][x] += user_class[ug]['demands'][y,x]
            user_class[ug]['demand_annual'][y + x*12] += user_class[ug]['demands'][y,x]
        #sum storage of individual user groups    
        total_storage['storage'][y + x*12] += user_class[ug]['storage'][y + x*12]
        
      #keep track of annual flow        
      annual_flow += (total_inflow[y,x] - total_evap[y,x]) * (1.0 - environmental_flow_portion)
      #find current day of water year
      if start_month > 9:
        dowy_now = (datetime(iteration_year, start_month, 1, 0 ,0) - datetime(iteration_year, 10, 1, 0 , 0)).days
      else:
        dowy_now = (datetime(iteration_year, start_month, 1, 0 ,0) - datetime(iteration_year - 1, 10, 1, 0, 0)).days
      
      #find flood storage pool in this timestep
      flood_storage, other = make_toy_demands.current_tocs(dowy_now, tocs_rule, total_fci[y,x])
      #set individual storage capacity based on current flood pool
      for ug in user_groups:
        if ug == cold_pool_category:
          user_class[ug]['capacity'][y + x*12] = cold_pool_storage
        else:
          user_class[ug]['capacity'][y + x*12] = user_class[ug]['storage_portion'] * ((flood_storage / 1000.0)  - cold_pool_storage)
      #set storage capacity equal to max flood capacity    
      total_storage['capacity'][y + x*12] = flood_storage / 1000.0
      #find releases made for flood pool storage
      flood_sim_releases = 0.0
      if flood_storage/1000.0 < total_storage['storage'][y + x*12]:
        flood_sim_releases = total_storage['storage'][y + x*12] - flood_storage/1000.0      
        total_storage['flood_release'][x] += flood_sim_releases
        total_storage['total_release'][y + x*12] += flood_sim_releases
      #can flood releases be captured by downstream storage?
      if flood_sim_releases > 0.0:
        off_site_storage += min(flood_sim_releases, off_site_diversion_capacity)
        off_site_storage = min(off_site_storage_capacity, off_site_storage)
        
        #which individual storage accounts are reduced for flood releases?
        total_over = 0.0
        for ug in user_groups:
          total_over += max(user_class[ug]['storage'][y + x*12] - user_class[ug]['capacity'][y + x*12], 0.0)        
        if total_over > 0.0:
          total_storage['storage'][y + x*12] = 0.0
          for ug in user_groups:
            user_class[ug]['storage'][y + x*12] -= max(user_class[ug]['storage'][y + x*12] - user_class[ug]['capacity'][y + x*12], 0.0) * min(flood_sim_releases / total_over, 1.0)
            user_class[ug]['storage_carryover'][y + x*12] -= min(max(user_class[ug]['storage'][y + x*12] - user_class[ug]['capacity'][y + x*12], 0.0) * min(flood_sim_releases / total_over, 1.0), user_class[ug]['storage_carryover'][y + x*12])
            total_storage['storage'][y + x*12] += user_class[ug]['storage'][y + x*12]

      #loop month and year values
      start_month += 1
      if start_month == 13:
        iteration_year += 1
        start_month = 1
  return total_storage, user_class

def get_missed_demands(user_class, total_storage, user_groups, water_year_types, environmental_category):
  total_missed = {}
  total_demand = {}
  for ug in user_groups:
    if ug == environmental_category:
      for class_use in ['_class1', '_class2']:
        total_missed[ug + class_use] = {}
        total_demand[ug + class_use] = {}
        for wyt in ['W', 'AN', 'BN', 'D', 'C']:
          total_missed[ug + class_use][wyt] = 0.0
          total_demand[ug + class_use][wyt] = 0.0
    else:
      total_missed[ug] = {}
      total_demand[ug] = {}
      for wyt in ['W', 'AN', 'BN', 'D', 'C']:
        total_missed[ug][wyt] = 0.0
        total_demand[ug][wyt] = 0.0
  total_missed['flood'] = {}
  total_missed['count'] = {}
  for wyt in ['W', 'AN', 'BN', 'D', 'C']:
    total_missed['flood'][wyt] = 0.0
    total_missed['count'][wyt] = 0.0
  for wyt_cnt, wyt in enumerate(water_year_types):
    total_missed['count'][wyt] += 1.0
    for ug in user_groups:
      if ug == environmental_category:
        total_missed[ug + '_class1'][wyt] += user_class[ug]['missed_class_1'][wyt_cnt]
        total_demand[ug + '_class1'][wyt] += user_class[ug]['demand_class_1'][wyt_cnt]
        for enviro_class in ['2', '3', '4']:
          total_missed[ug + '_class2'][wyt] += user_class[ug]['missed_class_' + enviro_class][wyt_cnt]
          total_demand[ug + '_class2'][wyt] += user_class[ug]['demand_class_' + enviro_class][wyt_cnt]
      else:
        total_missed[ug][wyt] += user_class[ug]['missed'][wyt_cnt]
        total_demand[ug][wyt] += user_class[ug]['demand'][wyt_cnt]
    total_missed['flood'][wyt] += total_storage['flood_release'][wyt_cnt]
  for wyt in ['W', 'AN', 'BN', 'D', 'C']:
    total_missed['flood'][wyt] = total_missed['flood'][wyt] / total_missed['count'][wyt]
  return total_missed, total_demand

def initialize_result_files(start_year, current_year):  
  datetime_index = []
  iteration_year = start_year - 1
  for x in range(0, current_year - start_year):
    start_month = 10
    for y in range(0,12):
      datetime_index.append(datetime(iteration_year, start_month, 1, 0 ,0))#create datetime index for results
      start_month += 1
      if start_month == 13:
        iteration_year += 1
        start_month = 1

  all_other_flows = pd.DataFrame()
  all_environmental_flows = pd.DataFrame(index = datetime_index)
  storage_allocations = pd.DataFrame(index = datetime_index)
  storage_release = pd.DataFrame(index = datetime_index)
  individual_storage_allocations = pd.DataFrame(index = datetime_index)
  individual_demands = pd.DataFrame(index = datetime_index)
  total_shortfalls_eco = pd.DataFrame()
  shortfall_by_wyt = pd.DataFrame()
  simplified_shortfalls = pd.DataFrame()
  expanded_shortfalls = pd.DataFrame()
  
  return all_other_flows, all_environmental_flows, storage_allocations, storage_release, individual_storage_allocations, individual_demands, total_shortfalls_eco, shortfall_by_wyt, simplified_shortfalls, expanded_shortfalls


def write_output_files(user_class, total_missed, total_demand, total_storage, all_other_flows, all_environmental_flows, storage_allocations, storage_release, individual_storage_allocations, individual_demands, total_shortfalls_eco, shortfall_by_wyt, simplified_shortfalls, expanded_shortfalls, user_groups, water_year_types, cold_pool_category, environmental_category, env_flow_portion_int, write_file = False):

  #create dictionary of group demands and shortfalls under each environmental flow scenario
  for ug in user_groups:
    individual_storage_allocations[ug + '_' + str(env_flow_portion_int)] = user_class[ug]['storage']
    if ug == environmental_category:
      individual_demands[ug] = user_class[ug]['demand_class_1_annual']
      for demand_class in ['2', '3', '4']:
        individual_demands[ug] += user_class[ug]['demand_class_' +  demand_class + '_annual']
    else:
      individual_demands[ug] = user_class[ug]['demand_annual']

  for ug in user_groups:
    if ug != cold_pool_category and ug != environmental_category:
      all_other_flows[ug] = user_class[ug]['demand'] * 1000.0      
      all_other_flows[ug + '_' + str(env_flow_portion_int*10)] = user_class[ug]['missed'] * 1000.0
      
  for enviro_class, label_name in zip(['1', '2', '3', '4'], ['missed_environmental_base', 'missed_spring_recession', 'missed_winter_peak', 'missed_fall_pulse']):
    all_environmental_flows[label_name + '_' + str(env_flow_portion_int*10)] = user_class[environmental_category]['missed_class_' + enviro_class + '_annual'] * 1000.0

  storage_allocations['total_storage_' + str(env_flow_portion_int*10)] = total_storage['storage'] * 1000.0
  storage_allocations['eco_storage_' + str(env_flow_portion_int*10)] = user_class[environmental_category]['storage'] * 1000.0
  storage_allocations['eco_storage_carryover' + str(env_flow_portion_int*10)] = user_class[environmental_category]['storage_carryover'] * 1000.0
  storage_allocations['total_release_' + str(env_flow_portion_int*10)] = total_storage['total_release'] * 1000.0    

  storage_release['Total Inflow (tAF/month)'] = total_storage['total_inflow'] * 1000.0
  storage_release['Total Release ' + str(env_flow_portion_int * 10) + '%'] = total_storage['total_release'] * 1000.0
  for env_count in range(1, 5):
    storage_release['Total Storage ' + str(env_flow_portion_int * 10) + '%'] = total_storage['storage'] * 1000.0
  
  for ug_cnt, ug in enumerate(user_groups):
    if ug == environmental_category:
      for wyt in ['W', 'AN', 'BN', 'D', 'C']:
        total_shortfalls_eco[ug + '_' + str(env_flow_portion_int) + wyt] = [total_missed[ug + '_class1'][wyt] + total_missed[ug + '_class2'][wyt],]

  for wyt_cnt, wyt in enumerate(['W', 'AN', 'BN', 'D', 'C']):
    for ug_cnt, ug in enumerate(user_groups):
      if ug != cold_pool_category and ug != environmental_category:
        shortfall_by_wyt.loc[env_flow_portion_int-1, ug + '_' + wyt] = total_missed[ug][wyt]/total_demand[ug][wyt]
      if ug == environmental_category:
        shortfall_by_wyt.loc[env_flow_portion_int-1, ug + '_class1_' + wyt] = total_missed[ug + '_class1'][wyt]/total_demand[ug + '_class1'][wyt]
        shortfall_by_wyt.loc[env_flow_portion_int-1, ug + '_class2_' + wyt] = total_missed[ug + '_class2'][wyt]/total_demand[ug + '_class2'][wyt]
        
        
  individual_demand = {}
  individual_shortage = {}
  for x in ['Salinity', 'In-Basin', 'Exports', 'Refuges']:
    individual_demand[x] = 0.0
    individual_shortage[x] = 0.0

  total_demand_env = 0.0
  total_missed_env = 0.0
  total_demand_other = 0.0
  total_missed_other = 0.0
  for wyt_cnt, wyt in enumerate(['W', 'AN', 'BN', 'D', 'C']):
    total_years_type = 0.0
    for x in water_year_types:
      if x == wyt:
        total_years_type += 1.0
    for ug_cnt, ug in enumerate(user_groups):
      if ug != cold_pool_category:
        if ug == environmental_category:
          total_missed_env += (total_missed[ug + '_class1'][wyt] + total_missed[ug + '_class2'][wyt]) * float(total_years_type)
          total_demand_env += (total_demand[ug + '_class1'][wyt] + total_demand[ug + '_class2'][wyt]) * float(total_years_type)
        else:
          total_missed_other += total_missed[ug][wyt] * float(total_years_type)
          total_demand_other += total_demand[ug][wyt] * float(total_years_type)
          individual_shortage[ug] += total_missed[ug][wyt] * float(total_years_type)
          individual_demand[ug] += total_demand[ug][wyt] * float(total_years_type)
            
  simplified_shortfalls.loc[env_flow_portion_int, 'other'] = 100.0*total_missed_other / total_demand_other
  simplified_shortfalls.loc[env_flow_portion_int, 'eco'] = 100.0*total_missed_env / total_demand_env
  for ug in user_groups:
    if ug != cold_pool_category and ug != environmental_category:
      expanded_shortfalls.loc[env_flow_portion_int - 1, ug] = 100 * individual_shortage[ug] / individual_demand[ug]
  
  return all_other_flows, all_environmental_flows, storage_allocations, storage_release, individual_storage_allocations, individual_demands, total_shortfalls_eco, shortfall_by_wyt, simplified_shortfalls, expanded_shortfalls

def save_output_files(all_other_flows, all_environmental_flows, storage_allocations, storage_release, individual_storage_allocations, individual_demands, total_shortfalls_eco, shortfall_by_wyt, simplified_shortfalls, expanded_shortfalls, off_site_diversion_capacity, cold_pool_storage, use_environmental_storage, output_folder):

  if use_environmental_storage:
    storage_filename = 'EWB_' + str(int(cold_pool_storage * 1000)) + '_with_storage_' + str(int(off_site_diversion_capacity * 1000000.0 /(1.98 * 30))) 
  else:
    storage_filename = 'pass_through_' + str(int(cold_pool_storage * 1000)) + '_with_storage_' + str(int(off_site_diversion_capacity * 1000000.0 /(1.98 * 30))) 
    
  individual_storage_allocations.to_csv(output_folder + 'individual_storage_allocations_' + storage_filename + '.csv')
  individual_demands.to_csv(output_folder + 'individual_demands_' + storage_filename + '.csv')
  
  if off_site_diversion_capacity == 0.0:
    all_environmental_flows.to_csv(output_folder + 'function_flow_demands_cold_pool_' + storage_filename + '.csv')
    all_other_flows.to_csv(output_folder + 'subgroup_demands_cold_pool_' + storage_filename + '.csv')
    storage_release.to_csv(output_folder + 'monthly_releases_' + storage_filename + '.csv')
  else:
    all_environmental_flows.to_csv(output_folder + 'function_flow_demands_cold_pool_' + storage_filename + '.csv')
    all_other_flows.to_csv(output_folder + 'subgroup_demands_cold_pool_' + storage_filename + '.csv')
    storage_release.to_csv(output_folder + 'monthly_releases_' + storage_filename + '.csv')  
  storage_allocations.to_csv(output_folder + 'storage_allocations_' + storage_filename + '.csv')
  
  total_shortfalls_eco.to_csv(output_folder + 'eco_shortfalls_' + storage_filename + '.csv')
  shortfall_by_wyt.to_csv(output_folder + 'shortfalls_by_wyt_' + storage_filename + '.csv')

  simplified_shortfalls.to_csv(output_folder + 'simplified_shortfalls_' + storage_filename + '.csv')
  expanded_shortfalls.to_csv(output_folder + 'expanded_shortfalls_' + storage_filename + '.csv')
  
