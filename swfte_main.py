from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from make_toy_plots import Plotter
import make_toy_demands
import make_toy_simulation

#set initial simulation parameters
start_year = 1996
current_year = 2022
show_plots = False
output_data_folder = 'swfte_output/'
figures_folder = 'swfte_figures/'

#list of water year types, 1996 - 2021
water_year_types = ['W', 'W', 'W', 'W', 'AN', 'D', 'D', 'AN', 'BN', 'AN', 'W', 'D', 'C', 'D', 'BN', 'W', 'BN', 'D', 'C', 'C', 'BN', 'W', 'BN', 'W', 'D', 'C']
wyt_cats = ['W', 'AN', 'BN', 'D', 'C']
#demand group names
real_list = ['junior', 'senior', 'delta', 'riparian', 'exports', 'refuges', 'environmental', 'coldpool', 'flood_release']#all individual users
stylized_list = ['Cold-Pool', 'Salinity', 'In-Basin', 'Refuges', 'Exports', 'Environment']#aggregated groups for plots
label_names = ['Cold-Pool', 'System', 'In-Basin',  'Refuges', 'Exports', 'Ecosystem\nWater\nBudget']#plotting names (with line breaks)
user_groups = stylized_list#demand group for analysis

#read in data about flow data and storage from Sacramento River to use as a scenario baseline
values = pd.read_csv('cord-sim_realtime_ppic.csv', index_col = 0)
values.index = pd.to_datetime(values.index)
flow_values = values.loc[datetime(start_year - 1, 10, 1, 0, 0):,:]
flow_values = flow_values[pd.notna(flow_values.index)]
initial_storage = flow_values.loc[flow_values.index[0], 'SHA_storage']/1000000.0
#use same inflow/evap for all simulations 
total_inflow, total_evap, total_fci = make_toy_simulation.get_total_inflow(flow_values, start_year, current_year)

#get delta water accounting for data on system/environmental water needs
eflows_ppic = pd.read_excel('ppic-delta-water-accounting.xlsx', sheet_name = 'Monthly Data', skiprows = 3)
eflows_ppic.index = pd.to_datetime(eflows_ppic['Date'])
eflows_values = eflows_ppic.loc[datetime(start_year - 1, 10, 1, 0, 0):,:]
eflows_values = eflows_values[pd.notna(eflows_values['*X2'])]

#get environmental rules to determine system/environmental water needs
delta_min_outflow, export_ratio, env_min_flow, temp_releases, tocs_rule = make_toy_demands.get_delta_rules()
x2_by_wyt, system_by_wyt = make_toy_demands.get_ppic_accounting(water_year_types, eflows_values, False)

#find user group demands
all_contractors = make_toy_demands.make_synthetic_demands(flow_values, real_list, start_year, current_year, tocs_rule, x2_by_wyt, system_by_wyt, water_year_types, show_plot = False)
all_contractors_wyt = make_toy_demands.make_synthetic_demands_by_wyt(real_list, water_year_types, all_contractors)
new_demands = make_toy_demands.make_stylized_demands(all_contractors, all_contractors_wyt, water_year_types, wyt_cats, start_year, current_year)
#get new functional flow demands
fish_timeseries, enviro_demands = make_toy_demands.get_fish_demands(all_contractors, start_year, current_year)

###INPUT DATA FIGURES
figure_A3 = Plotter('figure_A3', figsize1 = 12, figsize2 = 6)
figure_A3.plot_environmental_baseflow_as_pct_of_flow(all_contractors, flow_values, eflows_values, 'SHA', start_year, current_year, output_data_folder)
figure_A3.format_figure(figures_folder, 'svg')
del figure_A3
plot_type = 'stylized'
figure_A5 = Plotter('figure_A5', figsize1 = 6.4, figsize2 = 4.8)
figure_A5.plot_total_demand_by_wyt(real_list, wyt_cats, all_contractors_wyt, new_demands, plot_type, output_data_folder)
figure_A5.format_figure(figures_folder, 'svg')
del figure_A5
figure_A7 = Plotter('figure_A7', figsize1 = 12, figsize2 = 6)
figure_A7.plot_environmental_flow_types(all_contractors, fish_timeseries, start_year, current_year, output_data_folder)
figure_A7.format_figure(figures_folder, 'svg')
del figure_A7

#Initialize labels/dictionaries for simulation
environmental_category = 'Environment'
cold_pool_category = 'Cold-Pool'
second_class_category = ['Exports',]
off_site_storage_capacity = 1.0

#simulation parameters
use_class_2 = True
for off_site_diversion_capacity_cfs in [0.0, 500.0, 1000.0, 2500.0]:
  off_site_diversion_capacity = off_site_diversion_capacity_cfs * 1.98 * 30 / 1000000.0

  for use_environmental_storage in [True, False]:
    for cold_pool_storage in [0.0, 1.0, 1.25, 1.5]:
      #loop through simulations using different e-flow %
      all_other_flows, all_environmental_flows, storage_allocations, storage_release, individual_storage_allocations, individual_demands, total_shortfalls_eco, shortfall_by_wyt, simplified_shortfalls, expanded_shortfalls = make_toy_simulation.initialize_result_files(start_year, current_year)
      for env_count in range(1, 5):
        environmental_flow_portion = float(env_count) / 10.0
        total_storage, user_class = make_toy_simulation.initialize_simulation(start_year, current_year, environmental_flow_portion, initial_storage, cold_pool_storage, new_demands, enviro_demands, use_environmental_storage, use_class_2, user_groups, environmental_category, second_class_category, cold_pool_category)
        class_1_cutoff, class_2_total = make_toy_simulation.find_seniority_cutoffs(user_groups, user_class, second_class_category, environmental_category)
        total_storage, user_class = make_toy_simulation.run_simulation(user_class, environmental_flow_portion, cold_pool_storage, off_site_storage_capacity, off_site_diversion_capacity, start_year, current_year, user_groups, tocs_rule, total_storage, total_inflow, total_evap, total_fci, class_1_cutoff, class_2_total, environmental_category, second_class_category, cold_pool_category, use_environmental_storage)
        total_missed, total_demand = make_toy_simulation.get_missed_demands(user_class, total_storage, user_groups, water_year_types, environmental_category)  
        all_other_flows, all_environmental_flows, storage_allocations, storage_release, individual_storage_allocations, individual_demands, total_shortfalls_eco, shortfall_by_wyt, simplified_shortfalls, expanded_shortfalls = make_toy_simulation.write_output_files(user_class, total_missed, total_demand, total_storage, all_other_flows, all_environmental_flows, storage_allocations, storage_release, individual_storage_allocations, individual_demands, total_shortfalls_eco, shortfall_by_wyt, simplified_shortfalls, expanded_shortfalls, user_groups, water_year_types, cold_pool_category, environmental_category, env_count)
        if cold_pool_storage == 1.25 and env_count == 3 and use_environmental_storage and off_site_diversion_capacity == 0.0:
          figure_A6 = Plotter('figure_A6', figsize1 = 12, figsize2 = 12)
          figure_A6.make_storage_allocation_block(user_class, user_groups, label_names, cold_pool_storage, class_2_total, cold_pool_category, environmental_category, use_class_2, output_data_folder)
          figure_A6.format_figure(figures_folder, 'svg')
          del figure_A6
      make_toy_simulation.save_output_files(all_other_flows, all_environmental_flows, storage_allocations, storage_release, individual_storage_allocations, individual_demands, total_shortfalls_eco, shortfall_by_wyt, simplified_shortfalls, expanded_shortfalls, off_site_diversion_capacity, cold_pool_storage, use_environmental_storage, output_data_folder)


figure_A8 = Plotter('figure_A8_c_d', nr = 1, nc = 2, figsize1 = 15.2825, figsize2 = 4)
figure_A8.plot_partial_shortage_tradeoff('pass_through_0', output_data_folder)
figure_A8.format_figure(figures_folder, 'svg')
del figure_A8
figure_A9 = Plotter('figure_A9', figsize1 = 16, figsize2 = 6)
figure_A9.plot_storage_pass_through_flows('pass_through_0', output_data_folder)
figure_A9.format_figure(figures_folder, 'svg')
del figure_A9
figure_A11 = Plotter('figure_A11_c_d', nr = 1, nc = 2, figsize1 = 15.2825, figsize2 = 4)
figure_A11.plot_partial_shortage_tradeoff('pass_through_1250', output_data_folder)
figure_A11.format_figure(figures_folder, 'svg')
del figure_A11
figure_A12 = Plotter('figure_A12', figsize1 = 16, figsize2 = 6)
figure_A12.plot_storage_pass_through_flows('pass_through_1250', output_data_folder)
figure_A12.format_figure(figures_folder, 'svg')
del figure_A12
figure_A13 = Plotter('figure_A13', nr = 2, figsize1 = 16, figsize2 = 12)
figure_A13.plot_shortage_bar_charts('pass_through', output_data_folder)
figure_A13.format_figure(figures_folder, 'svg')
del figure_A13
figure_A14 = Plotter('figure_A14', figsize1 = 16, figsize2 = 12)
figure_A14.plot_shortfall_tradeoffs(2, output_data_folder)
figure_A14.format_figure(figures_folder, 'svg')
del figure_A14
figure_A15 = Plotter('figure_A15_c_d', nr = 1, nc = 2, figsize1 = 15.2825, figsize2 = 4)
figure_A15.plot_partial_shortage_tradeoff('EWB_0', output_data_folder)
figure_A15.format_figure(figures_folder, 'svg')
del figure_A15
figure_A16 = Plotter('figure_A16_c_d', nr = 1, nc = 2, figsize1 = 15.2825, figsize2 = 4)
figure_A16.plot_partial_shortage_tradeoff('EWB_1250', output_data_folder)
figure_A16.format_figure(figures_folder, 'svg')
del figure_A16
figure_A17 = Plotter('figure_A17', nr = 2, figsize1 = 16, figsize2 = 12)
figure_A17.plot_temperature_attainment(output_data_folder)
figure_A17.format_figure(figures_folder, 'svg')
del figure_A17
figure_A18 = Plotter('figure_A18', nr = 4, figsize1 = 16.6, figsize2 = 14.2)
figure_A18.plot_individual_storage_allocations(4, output_data_folder)
figure_A18.format_figure(figures_folder, 'svg', use_tight_layout = True)
del figure_A18
figure_A21 = Plotter('figure_A21', nr = 4, figsize1 = 16, figsize2 = 20)
figure_A21.plot_shortage_bar_charts('EWB', output_data_folder)
figure_A21.format_figure(figures_folder, 'svg')
del figure_A21
figure_A22 = Plotter('figure_A22', nr = 4, figsize1 = 16, figsize2 = 20)
figure_A22.plot_shortage_bar_charts('all', output_data_folder)
figure_A22.format_figure(figures_folder, 'svg')
del figure_A22
figure_A23 = Plotter('figure_A23', figsize1 = 16, figsize2 = 12)
figure_A23.plot_shortfall_tradeoffs(4, output_data_folder)
figure_A23.format_figure(figures_folder, 'svg')
del figure_A23
figure_A24 = Plotter('figure_A24', figsize1 = 16, figsize2 = 6)
figure_A24.plot_shortage_with_off_site_storage(output_data_folder)
figure_A24.format_figure(figures_folder, 'svg')
del figure_A24

