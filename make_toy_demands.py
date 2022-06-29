from datetime import datetime, timedelta
from calendar import monthrange
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def current_tocs(dowy, tocs_rule, ix):
##Interpolates rules from tocs_rule in *_properties.json file to get the top of the conservation
##pool in order to determine flood control releases in reservoir.step
  for i,v in enumerate(tocs_rule['index']):
    if ix > v:
      break
  storage_bounds = np.zeros(2)
  index_bounds = np.zeros(2)
  day_bounds = np.ones(2)*4552.0
  for x, y in enumerate(tocs_rule['dowy'][i-1]):
    if dowy < y:
      day_bounds[1] = min(day_bounds[1], tocs_rule['storage'][i-1][x])
  for x, y in enumerate(tocs_rule['dowy'][i]):
    if dowy < y:
      day_bounds[0] = min(day_bounds[0], tocs_rule['storage'][i][x])
		
  storage_bounds[1] = np.interp(dowy, tocs_rule['dowy'][i-1], tocs_rule['storage'][i-1])
  storage_bounds[0] = np.interp(dowy, tocs_rule['dowy'][i], tocs_rule['storage'][i])
  index_bounds[1] = tocs_rule['index'][i-1]
  index_bounds[0] = tocs_rule['index'][i]
  return np.interp(ix, index_bounds, storage_bounds), np.interp(ix, index_bounds, day_bounds)


def make_synthetic_demands(values, water_group_types, start_year, current_year, tocs_rule, x2_by_wyt, system_by_wyt, water_year_types, show_plot = False):
  #this function distributes releases from Shasta Reservoir to different demand groups on the Sacramento R.
  #to serve as a basis for the simulation demands

  #read in historical deliveries to Sacramento River CVP contractors from the:
  #Tehmama-Colousa, Sacramento River Settlement, Delta/Medota, and San Luis unit
  cvp_contractors = {}
  groups_from_cvp = ['tehamacolusa', 'sac_settlement', 'deltamendota', 'sanluis']
  for x in groups_from_cvp:
    cvp_contractors[x] = pd.read_csv(x + '.csv', index_col = 0)
    cvp_contractors[x].index = pd.to_datetime(cvp_contractors[x].index)
    cvp_contractors[x + '_array'] = np.zeros((12, current_year - start_year + 1))
    for index, row in cvp_contractors[x].iterrows():
      if index.month > 9:
        month_num = index.month - 10
        year_num = index.year - (start_year - 1)
      else:
        month_num = index.month + 2
        year_num = index.year - start_year
      cvp_contractors[x + '_array'][month_num, year_num] += row['diversions']/1000000.0
    
  #store timeseries of group demands
  all_contractors = {}
  all_contractors['all_environmental'] = np.zeros((12, current_year - start_year + 1))#2D monthly
  all_contractors['all_environmental_timeseries'] = np.zeros(12*(current_year - start_year + 1))#1D monthly
  for x in water_group_types:
    all_contractors[x] = np.zeros((12, current_year - start_year + 1))#2D monthly
    all_contractors[x + '_timeseries'] = np.zeros(12*(current_year - start_year + 1))#1D monthly

  #check to make sure all flow released from Shasta is distributed to individual demands
  total_flow_use = np.zeros(len(values))

  #make a date index with years from October - September
  all_contractors['date_index'] = []
  month_num = 10
  year_num = start_year - 1
  while year_num < current_year or month_num < 10:
    all_contractors['date_index'].append(datetime(year_num, month_num, 1, 0, 0))
    month_num += 1
    if month_num == 13:
      month_num = 1
      year_num += 1
  counter = 0
  
  #loop through daily data from Shasta Reservoir
  for index, row in values.iterrows():
    if index.month > 9:
      month_num = index.month - 10
      year_num = index.year - (start_year - 1)
      dowy_now = (index - datetime(index.year, 10, 1, 0 , 0)).days
      day_num = index.day
    else:
      month_num = index.month + 2
      year_num = index.year - start_year
      day_num = index.day
      dowy_now = (index - datetime(index.year - 1, 10, 1, 0, 0)).days

    #find top of flood pool
    flood_storage, other = current_tocs(dowy_now, tocs_rule, row['SHA_fci'])  
    
    #get releases for system/environmental water
    if year_num >= len(water_year_types):
      wyt = water_year_types[-1]
    else:
      wyt = water_year_types[year_num]
      
    #ESTIMATE ALL E-FLOW DEMAND
    #standard delta outflow is 'system' water, other X2 releases are environmental
    delta_outflow_release = system_by_wyt[wyt][month_num] /(1000.0*float(monthrange(index.year, index.month)[1]))
    x2_release = max(x2_by_wyt[wyt][month_num] /(1000.0*float(monthrange(index.year, index.month)[1])) - delta_outflow_release, 0.0)
    all_contractors['all_environmental'][month_num, year_num] += x2_release
    all_contractors['all_environmental_timeseries'][month_num + year_num*12] += x2_release
    
    #if flood storage is encroached all releases assigned to flood, otherwise they go to individual demand groups
    if flood_storage < row['SHA_storage']/1000.0:
      #FLOOD
      all_contractors['flood_release'][month_num, year_num] += row['SHA_otf'] * 1.98/1000000.0
      all_contractors['flood_release_timeseries'][month_num + year_num*12] += row['SHA_otf'] * 1.98/1000000.0
    else:
      #total release to be distributed (i.e., sum of total demands is set equal to this value)
      total_toy_release = row['SHA_otf'] * 1.98/1000000.0
      
      ###IN-BASIN
      #JUNIOR IN-BASIN
      #get diversions for tehama/colusa canal, these diversions are 'junior' users
      tehama_diversion = min(cvp_contractors['tehamacolusa_array'][month_num, year_num] / float(monthrange(index.year, index.month)[1]), total_toy_release - total_flow_use[counter])
      all_contractors['junior'][month_num, year_num] += tehama_diversion 
      all_contractors['junior_timeseries'][month_num + year_num*12] += tehama_diversion
      total_flow_use[counter] += tehama_diversion
      
      #SENIOR IN-BASIN
      #get diversions for sacramento settlement contractors, these diversions are 'senior' users
      sac_settlement_diversion = min(cvp_contractors['sac_settlement_array'][month_num, year_num] / float(monthrange(index.year, index.month)[1]), total_toy_release - total_flow_use[counter])
      all_contractors['senior'][month_num, year_num] += sac_settlement_diversion
      all_contractors['senior_timeseries'][month_num + year_num*12] += sac_settlement_diversion
      total_flow_use[counter] += sac_settlement_diversion

      ###DELTA
      #inflows from major tributaries into the 'delta' region to ensure there is enough other water for non-CVP users
      total_other_water = max(tehama_diversion + sac_settlement_diversion + row['SHA_gains'] * 1.98/1000000.0,0.0)
      for res in ['ORO', 'YRS', 'FOL', 'NML', 'DNP', 'EXC']:
        total_other_water += (row[res + '_otf'] + row[res + '_gains'])*1.98/1000000.0
      for sta in ['SAC', 'SJ', 'EAST']:
        total_other_water += row[sta + '_gains']*1.98/1000000.0
      #delta outflow demands are split into system and environmental water
      delta_outflow_release = system_by_wyt[wyt][month_num] /(1000.0*float(monthrange(index.year, index.month)[1]))
      x2_release = max(x2_by_wyt[wyt][month_num] /(1000.0*float(monthrange(index.year, index.month)[1])) - delta_outflow_release, 0.0)
       
      #ENVIRONMENTAL
      #environmental water demands
      all_contractors['environmental'][month_num, year_num] += min(x2_release, total_toy_release - total_flow_use[counter])
      all_contractors['environmental_timeseries'][month_num + year_num*12] += min(x2_release, total_toy_release - total_flow_use[counter])
      if x2_release > total_toy_release - total_flow_use[counter]:
        total_other_water -= x2_release - (total_toy_release - total_flow_use[counter])
      total_flow_use[counter] += min(x2_release, total_toy_release - total_flow_use[counter])
              
      #SYSTEM - DELTA
      #system water demands
      all_contractors['delta'][month_num, year_num] += min(delta_outflow_release,total_toy_release - total_flow_use[counter])
      all_contractors['delta_timeseries'][month_num + year_num*12] += min(delta_outflow_release,total_toy_release - total_flow_use[counter])
      if delta_outflow_release > total_toy_release - total_flow_use[counter]:
        total_other_water -= delta_outflow_release - (total_toy_release - total_flow_use[counter])
      total_flow_use[counter] += min(delta_outflow_release, total_toy_release - total_flow_use[counter])      
            
      ####SOUTH-OF DELTA
      #check to see if SWP/delta island demands are using water from Shasta
      for daily_obs, user_group_member, unit_value in zip(['HRO_pump', 'delta_depletions'], ['exports', 'riparian'], [1.98/1000000.0, -1.98/1000000.0]):
        if total_other_water > row[daily_obs] * unit_value:
          total_other_water -= row[daily_obs] * unit_value
        else:
          group_diversion = min(max(row[daily_obs] * unit_value, 0.0) - total_other_water, total_toy_release - total_flow_use[counter])
          all_contractors[user_group_member][month_num, year_num] += group_diversion
          all_contractors[user_group_member + '_timeseries'][month_num + year_num*12] += group_diversion
          total_flow_use[counter] += group_diversion
          total_other_water = 0.0         
      #pumping through CVP pumps are split into 'exports' and 'refugres'
      this_step_pumping = max(row['TRP_pump'] * 1.98 / 1000000.0, 0.0)

      #REFUGE
      #estimated refuge demands from 550taf/year
      if month_num == 0 and day_num == 1:
        total_refuge = 0.555
        refuge_ratio = 0.0
        for x in ['deltamendota', 'sanluis']:
          refuge_ratio += np.sum(cvp_contractors[x + '_array'][:, year_num])
        value_ratio = total_refuge/refuge_ratio 
      obs_refuge = 0.0
      for x in ['deltamendota', 'sanluis']:
        obs_refuge += cvp_contractors[x + '_array'][month_num, year_num]* value_ratio
      total_refuge_pumping = min(total_refuge, this_step_pumping, obs_refuge)
      total_refuge -= total_refuge_pumping      
      all_contractors['refuges'][month_num, year_num] += total_refuge_pumping
      all_contractors['refuges_timeseries'][month_num + year_num*12] += total_refuge_pumping

      #EXPORT
      #exports are pumping minum estimated refuge demands
      all_contractors['exports'][month_num, year_num] += this_step_pumping - total_refuge_pumping
      all_contractors['exports_timeseries'][month_num + year_num*12] += this_step_pumping - total_refuge_pumping
    
      total_other_water -= row['TRP_pump'] * 1.98/1000000.0 - this_step_pumping
      total_flow_use[counter] += this_step_pumping
      too_much_water = max(total_flow_use[counter] - total_toy_release, 0.0)
      total_this_month = 0.0
      for name_type in ['exports', 'senior', 'junior', 'delta']:
        total_this_month += all_contractors[name_type][month_num, year_num]
      if total_this_month > too_much_water:
        for name_type in ['exports', 'senior', 'junior', 'delta']:
          all_contractors[name_type][month_num, year_num] -= all_contractors[name_type][month_num, year_num] * (too_much_water / total_this_month)
      else:
        for name_type in ['exports', 'senior', 'junior', 'delta']:
          all_contractors[name_type][month_num, year_num] -= 0.0
      
      total_flow_use[counter] += max(total_toy_release - total_flow_use[counter], 0.0)
    
    counter += 1
    
  return all_contractors

def make_synthetic_demands_by_wyt(water_group_types, water_year_types, all_contractors):
  #Record total delivery by water year type for each demand group
  wyt_cats = ['W', 'AN', 'BN', 'D', 'C']
  all_contractors_wyt = {}
  for x in water_group_types:
    all_contractors_wyt[x] = {}
    for wyt in wyt_cats:
      all_contractors_wyt[x][wyt] = []    
    for wyt_cnt, wyt in enumerate(water_year_types):
      all_contractors_wyt[x][wyt].append(np.sum(all_contractors[x][:,wyt_cnt]))

  return all_contractors_wyt

def make_stylized_demands(all_contractors, all_contractors_wyt, water_year_types, wyt_cats, start_year, current_year):
  stylized_list = ['In-Basin', 'Exports', 'Salinity', 'Refuges']
  new_demands = {}
  for x in stylized_list:
    new_demands[x] = {}
    new_demands[x]['monthly'] = np.zeros((12, current_year - start_year + 1))

  #link aggregated groups to disaggregated groups
  new_demands['In-Basin']['type_list'] = ['junior', 'senior', 'riparian']
  new_demands['Exports']['type_list'] = ['exports',]
  new_demands['Salinity']['type_list'] = ['delta',]
  new_demands['Refuges']['type_list'] = ['refuges',]

  #make distribution of annual demands a function of observed trends by wyt
  for wyt_cnt, wyt in enumerate(wyt_cats):
    for x in stylized_list:
      new_demands[x][wyt] = 0.0
      for xx in new_demands[x]['type_list']:
        new_demands[x][wyt] += np.mean(np.asarray(all_contractors_wyt[xx][wyt]))
        
  #get overall demand in each large group
  total_stylized_demand = 0.0
  for x in stylized_list:
    for wyt in wyt_cats:
      total_stylized_demand += new_demands[x][wyt]
      
  #set refuge demands to 555/422 taf per year based on wyt
  total_refuge_demand = 0.0
  for wyt in ['W', 'AN']:
    new_demands['Refuges'][wyt] = 0.555
  for wyt in ['BN', 'D', 'C']:
    new_demands['Refuges'][wyt] = 0.422
  for wyt in wyt_cats:
    total_refuge_demand += new_demands['Refuges'][wyt]
    
  #assign all non-refuge demands equal overall volumes across 5 water-year-types
  for x in stylized_list:
    if x != 'Refuges':        
      total_user_demand = 0.0
      for wyt in wyt_cats:
        total_user_demand += new_demands[x][wyt]
      for wyt in wyt_cats:
        new_demands[x][wyt] = new_demands[x][wyt] * (total_stylized_demand - total_refuge_demand)  / ( total_user_demand * (len(stylized_list) - 1) )
        
    #use monthly distribution of annual demand that reflects observed values
    for wyt_cnt, wyt in enumerate(water_year_types):
      for monthnum in range(0,12):
        for xx in new_demands[x]['type_list']:
          new_demands[x]['monthly'][monthnum, wyt_cnt] +=  all_contractors[xx][monthnum, wyt_cnt]
      for monthnum in range(0,12):
        new_demands[x]['monthly'][monthnum, wyt_cnt] = new_demands[x]['monthly'][monthnum, wyt_cnt] * new_demands[x][wyt] / np.sum(new_demands[x]['monthly'][:, wyt_cnt])
  
  return new_demands
    
    
def get_ppic_accounting(water_year_types, eflows_ppic, show_plot):
  #
  x2_values = np.zeros((12, 26))
  other_system = np.zeros((12,26))
  for index, row in eflows_ppic.iterrows():
    if index.month > 9:
      month_num = index.month - 10
      year_num = index.year - 1995
    else:
      month_num = index.month + 2
      year_num = index.year - 1996
    #divide system water into X2 and 'other'
    x2_values[month_num][year_num] += np.max(np.asarray([row['*X2'], row['*PP'], row['*Jan'], row['*Jul-Aug-Sep'], row['*Oct-Nov-Dec']])) + row['Fish Xchan cost']
    other_system[month_num][year_num] += np.max(np.asarray([row['Tracy 250'], row['RS 250'] + row['CW M&I'], row['RS/Ant 150'] + row['CW M&I'], row['Emm'], row['JP'] + row['CW Ag'], row['Term/SAL'] + row['CW Ag']]))
    
  x2_by_wyt = {}
  system_by_wyt = {}
  color_vals = {}
  wyt_list = ['W', 'AN', 'BN', 'D', 'C']
  color_list = ['navy', 'steelblue', 'goldenrod', 'indianred', 'crimson']
  for wyt, color_use in zip(wyt_list,color_list):
    color_vals[wyt] = color_use
    system_by_wyt[wyt] = np.zeros(12)
    x2_by_wyt[wyt] = np.zeros(12)
    x2_by_wyt[wyt + '_cnt'] = 0.0
  for x_cnt, wyt in enumerate(water_year_types):
    if np.sum(x2_values[:, x_cnt]) == 0.0:
      break
    else:
      for month_num in range(0,12):
        x2_by_wyt[wyt][month_num] += x2_values[month_num, x_cnt]
        system_by_wyt[wyt][month_num] += other_system[month_num, x_cnt]
      x2_by_wyt[wyt + '_cnt'] += 1.0
  fig, ax = plt.subplots(2) 
  for wyt in wyt_list:
    x2_by_wyt[wyt] = x2_by_wyt[wyt] / x2_by_wyt[wyt + '_cnt']
    system_by_wyt[wyt] = system_by_wyt[wyt] / x2_by_wyt[wyt + '_cnt']
    ax[0].plot(x2_by_wyt[wyt], color = color_vals[wyt])
    ax[1].plot(system_by_wyt[wyt], color = color_vals[wyt])
  if show_plot:
    plt.show()
  return x2_by_wyt, system_by_wyt
  
def get_delta_rules():

  #database of delta rules used to make basin demands
  delta_min_outflow = {
      "W": [6000,7100,7100,7100,7100,7100,8000,4000,3000,4000,4500,4500],
      "AN": [6000,7100,7100,7100,7100,7100,8000,4000,3000,4000,4500,4500],
      "BN": [6000,7100,7100,7100,7100,7100,6500,4000,3000,4000,4500,4500],
      "D": [6000,7100,7100,7100,7100,7100,5000,3500,3000,4000,4500,4500],
      "C": [4500,7100,7100,7100,7100,7100,4000,3000,3000,3000,3500,3500]
    }
  export_ratio = {
      "W": [0.65,0.35,0.35,0.35,0.35,0.35,0.65,0.65,0.65,0.65,0.65,0.65],
      "AN": [0.65,0.35,0.35,0.35,0.35,0.35,0.65,0.65,0.65,0.65,0.65,0.65],
      "BN": [0.65,0.40,0.35,0.35,0.35,0.35,0.65,0.65,0.65,0.65,0.65,0.65],
      "D": [0.65,0.40,0.35,0.35,0.35,0.35,0.65,0.65,0.65,0.65,0.65,0.65],
      "C": [0.65,0.45,0.35,0.35,0.35,0.35,0.65,0.65,0.65,0.65,0.65,0.65]
    }
  env_min_flow = {
      "W": [3250,3250,2300,2300,2300,2300,2300,2300,3250,3250,3250,3250],
      "AN": [3250,3250,2300,2300,2300,2300,2300,2300,3250,3250,3250,3250],
      "BN": [3250,3250,2300,2300,2300,2300,2300,2300,3250,3250,3250,3250],
      "D":  [3250,3250,2300,2300,2300,2300,2300,2300,3250,3250,3250,3250],
      "C":  [2000,2000,2300,2300,2300,2300,2300,2300,2800,2800,2800,2000]
    }
  temp_releases = {
      "W": [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000],
      "AN": [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000],
      "BN": [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000],
      "D": [5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000],
      "C": [3250, 3250, 3250, 3250, 3250, 3250, 3250, 3250, 3250, 3250, 3250, 3250]
    }
  
  tocs_rule = {
      "index": [9999999,530000,500000,400000,300000,200000,110000,0],
      "dowy":  [[0,60,84,170,257,366],
                [0,60,84,170,257,366],
                [0,60,84,170,250,366],
                [0,60,84,170,230,366],
                [0,60,84,170,208,366],
                [0,60,84,170,188,366],
                [0,60,84,170,366],
                [0,60,84,170,366]],
      "storage": [[4552,3252,3252,3252,4552,4552],
                  [4552,3252,3252,3252,4552,4552],
                  [4552,3252,3252,3352,4552,4552],
                  [4552,3252,3252,3652,4552,4552],
                  [4552,3252,3252,3992,4552,4552],
                  [4552,3252,3252,4292,4552,4552],
                  [4552,3252,3252,4552,4552],
                  [4552,3252,3252,4552,4552]]
    }
  
  return delta_min_outflow, export_ratio, env_min_flow, temp_releases, tocs_rule
  
def get_fish_demands(all_contractors, start_year, current_year):

  fish_priorities = {}
  fish_priorities['2'] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 99.15, 99.15, 99.15, 0.0, 0.0, 0.0]
  fish_priorities['3'] = [0.0, 0.0, 0.0, 130.722, 130.722, 130.722, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  fish_priorities['4'] = [24.7, 24.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
  counter = 0
  month_num = 0
  year_num = 0
  fish_timeseries = {}
  enviro_demands = {}
  enviro_demands['class1'] = all_contractors['environmental'] * 1.0
  for x in fish_priorities:
    fish_timeseries[x] = np.zeros((current_year - start_year + 1) * 12)
    enviro_demands['class' + x] = np.zeros((12, current_year - start_year + 1))
  for x in range(0, (current_year - start_year + 1) * 12):
    for xx in fish_priorities:
      fish_timeseries[xx][x] = fish_priorities[xx][month_num] * 1.0
      enviro_demands['class' + xx][month_num,year_num] = fish_priorities[xx][month_num] / 1000.0
    month_num += 1
    if month_num ==12:
      month_num = 0
      year_num += 1
                   
  return fish_timeseries, enviro_demands