import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Circle
import matplotlib.ticker as mtick

class Plotter():
  def __init__(self, filename, nr = 1, nc = 0, figsize1 = 20, figsize2 = 16):
    self.sub_rows = nr
    self.sub_cols = nc
    self.filename = filename
    if self.sub_cols == 0:
      self.fig, self.ax = plt.subplots(self.sub_rows, figsize=(figsize1,figsize2))
      if self.sub_rows == 1:
        self.xlim = []
        self.ylim = []
        self.ylabel = 'none'
        self.xlabel = 'none'
        self.legend_title = 'none'
        self.xtick_locations = []
        self.xtick_labels = []
        self.ytick_locations = []
        self.ytick_labels = []
        self.legend_elements = []
        self.legend_location = 'upper left'
        self.legend_columns = 1
        self.legend_title = 'none'
        self.ylabelsize = 16
        self.xlabelsize = 16
        self.tickfontsize = 0
        self.legend_fontsize = 16
        self.legend_title_fontsize = 16
        self.xticks = 'keep'
        self.yticks = 'keep'
        self.tickfont = 'Gill Sans MT'
        self.type = 'single'
        self.ax.grid(False)
      else:
        self.type = '1d'
        self.xlim = {}
        self.ylim = {}
        self.ylabel = {}
        self.xlabel = {}
        self.legend_title = {}
        self.xtick_locations = {}
        self.xtick_labels = {}
        self.ytick_locations = {}
        self.ytick_labels = {}
        self.legend_elements = {}
        self.legend_location = {}
        self.legend_columns = {}
        self.legend_title = {}
        self.ylabelsize = {}
        self.xlabelsize = {}
        self.tickfontsize = {}
        self.legend_fontsize = {}
        self.legend_title_fontsize = {}
        self.xticks = {}
        self.yticks = {}
        self.tickfont = {}
        for x in range(0, self.sub_rows):
          self.xlim[str(x)] = []
          self.ylim[str(x)] = []
          self.ylabel[str(x)] = 'none'
          self.xlabel[str(x)] = 'none'
          self.legend_title[str(x)] = 'none'
          self.xtick_locations[str(x)] = []
          self.xtick_labels[str(x)] = []
          self.ytick_locations[str(x)] = []
          self.ytick_labels[str(x)] = []
          self.legend_elements[str(x)] = []
          self.legend_location[str(x)] = 'upper left'
          self.legend_columns[str(x)] = 1
          self.legend_title[str(x)] = 'none'
          self.ylabelsize[str(x)] = 16
          self.xlabelsize[str(x)] = 16
          self.tickfontsize[str(x)] = 0
          self.legend_fontsize[str(x)] = 16
          self.legend_title_fontsize[str(x)] = 16
          self.xticks[str(x)] = 'keep'
          self.yticks[str(x)] = 'keep'
          self.tickfont[str(x)] = 'Gill Sans MT'
          self.ax[x].grid(False)
    else: 
      self.fig, self.ax = plt.subplots(self.sub_rows, self.sub_cols, figsize=(figsize1, figsize2))
      self.type = '2d'
      self.type = '1d'
      self.xlim = {}
      self.ylim = {}
      self.ylabel = {}
      self.xlabel = {}
      self.legend_title = {}
      self.xtick_locations = {}
      self.xtick_labels = {}
      self.ytick_locations = {}
      self.ytick_labels = {}
      self.legend_elements = {}
      self.legend_location = {}
      self.legend_columns = {}
      self.legend_title = {}
      self.ylabelsize = {}
      self.xlabelsize = {}
      self.tickfontsize = {}
      self.legend_fontsize = {}
      self.legend_title_fontsize = {}
      self.xticks = {}
      self.yticks = {}
      self.tickfont = {}
      for x in range(0, self.sub_rows):
        self.xlim[str(x)] = {}
        self.ylim[str(x)] = {}
        self.ylabel[str(x)] = {}
        self.xlabel[str(x)] = {}
        self.legend_title[str(x)] = {}
        self.xtick_locations[str(x)] = {}
        self.xtick_labels[str(x)] = {}
        self.ytick_locations[str(x)] = {}
        self.ytick_labels[str(x)] = {}
        self.legend_elements[str(x)] = {}
        self.legend_location[str(x)] = {}
        self.legend_columns[str(x)] = {}
        self.legend_title[str(x)] = {}
        self.ylabelsize[str(x)] = {}
        self.xlabelsize[str(x)] = {}
        self.tickfontsize[str(x)] = {}
        self.legend_fontsize[str(x)] = {}
        self.legend_title_fontsize[str(x)] = {}
        self.xticks[str(x)] = {}
        self.yticks[str(x)] = {}
        self.tickfont[str(x)] = {}
        for y in range(0, self.sub_cols):
          self.xlim[str(x)][str(y)] = []
          self.ylim[str(x)][str(y)] = []
          self.ylabel[str(x)][str(y)] = 'none'
          self.xlabel[str(x)][str(y)] = 'none'
          self.legend_title[str(x)][str(y)] = 'none'
          self.xtick_locations[str(x)][str(y)] = []
          self.xtick_labels[str(x)][str(y)] = []
          self.ytick_locations[str(x)][str(y)] = []
          self.ytick_labels[str(x)][str(y)] = []
          self.legend_elements[str(x)][str(y)] = []
          self.legend_location[str(x)][str(y)] = 'upper left'
          self.legend_columns[str(x)][str(y)] = 1
          self.legend_title[str(x)][str(y)] = 'none'
          self.ylabelsize[str(x)][str(y)] = 16
          self.xlabelsize[str(x)][str(y)] = 16
          self.tickfontsize[str(x)][str(y)] = 0
          self.legend_fontsize[str(x)][str(y)] = 16
          self.legend_title_fontsize[str(x)][str(y)] = 16
          self.xticks[str(x)][str(y)] = 'keep'
          self.yticks[str(x)][str(y)] = 'keep'
          self.tickfont[str(x)][str(y)] = 'Gill Sans MT'
          
          
          self.ax[x].grid(False)

  def format_figure(self, figure_folder, file_type, ylabel = '', fontsize = 0, labelsize = 0, use_tight_layout = False, show_plots = False):
    #Set axis bounds
    if self.sub_cols == 0:
      if self.sub_rows == 1:
        if len(self.xlim) > 0:
          self.ax.set_xlim(self.xlim)
        if len(self.ylim) > 0:
          self.ax.set_ylim(self.ylim)
      
        #Set axis ticks
        if self.xticks == 'remove':
          self.ax.set_xticks([])
          self.ax.set_xticklabels('')
        else:
          if len(self.xtick_locations) > 0:
            self.ax.set_xticks(self.xtick_locations)
          if len(self.xtick_labels) > 0:
            self.ax.set_xticklabels(self.xtick_labels)
        if self.yticks == 'remove':
          self.ax.set_yticks([])
          self.ax.set_yticklabels('')
        else:
          if len(self.ytick_locations) > 0:
            self.ax.set_yticks(self.ytick_locations)
          if len(self.ytick_labels) > 0:
            self.ax.set_yticklabels(self.ytick_labels)
        for tick in self.ax.get_xticklabels():
          if self.tickfont != 'none':
            tick.set_fontname(self.tickfont)
          if self.tickfontsize > 0:
            tick.set_fontsize(self.tickfontsize)
        for tick in self.ax.get_yticklabels():
          if self.tickfont != 'none':
            tick.set_fontname(self.tickfont)
          if self.tickfontsize > 0:
            tick.set_fontsize(self.tickfontsize)
        
        #Set axis labels
        if self.ylabel != 'none':
          self.ax.set_ylabel(self.ylabel, fontsize = self.ylabelsize, weight = 'bold', fontname = 'Gill Sans MT')
        if self.xlabel != 'none':
          self.ax.set_xlabel(self.xlabel, fontsize = self.xlabelsize, weight = 'bold', fontname = 'Gill Sans MT')
      
        #Set plot legend  
        if len(self.legend_elements) > 0:
          if self.legend_title == 'none':
            self.ax.legend(handles = self.legend_elements, loc = self.legend_location, ncol = self.legend_columns, prop={'family':'Gill Sans MT','weight':'bold','size':self.legend_fontsize}) 
          else:
            self.ax.legend(handles = self.legend_elements, loc = self.legend_location, ncol = self.legend_columns, title=self.legend_title, title_fontsize = self.legend_title_fontsize, prop={'family':'Gill Sans MT','weight':'bold','size':self.legend_fontsize}) 
      else:
        for axis_r in range(0, self.sub_rows):
          if len(self.xlim[str(axis_r)]) > 0:
            self.ax[axis_r].set_xlim(self.xlim[str(axis_r)])
          if len(self.ylim[str(axis_r)]) > 0:
            self.ax[axis_r].set_ylim(self.ylim[str(axis_r)])
      
          #Set axis ticks
          if self.xticks[str(axis_r)] == 'remove':
            self.ax[axis_r].set_xticks([])
            self.ax[axis_r].set_xticklabels('')
          else:
            if len(self.xtick_locations[str(axis_r)]) > 0:
              self.ax[axis_r].set_xticks(self.xtick_locations[str(axis_r)])
            if len(self.xtick_labels[str(axis_r)]) > 0:
              self.ax[axis_r].set_xticklabels(self.xtick_labels[str(axis_r)])
          if self.yticks[str(axis_r)] == 'remove':
            self.ax[axis_r].set_yticks([])
            self.ax[axis_r].set_yticklabels('')
          else:
            if len(self.ytick_locations[str(axis_r)]) > 0:
              self.ax[axis_r].set_yticks(self.ytick_locations[str(axis_r)])
            if len(self.ytick_labels[str(axis_r)]) > 0:
              self.ax[axis_r].set_yticklabels(self.ytick_labels[str(axis_r)])
          for tick in self.ax[axis_r].get_xticklabels():
            if self.tickfont[str(axis_r)] != 'none':
              tick.set_fontname(self.tickfont[str(axis_r)])
            if self.tickfontsize[str(axis_r)] > 0:
              tick.set_fontsize(self.tickfontsize[str(axis_r)])
          for tick in self.ax[axis_r].get_yticklabels():
            if self.tickfont[str(axis_r)] != 'none':
              tick.set_fontname(self.tickfont[str(axis_r)])
            if self.tickfontsize[str(axis_r)] > 0:
              tick.set_fontsize(self.tickfontsize[str(axis_r)])
        
          #Set axis labels
          if self.ylabel[str(axis_r)] != 'none':
            self.ax[axis_r].set_ylabel(self.ylabel[str(axis_r)], fontsize = self.ylabelsize[str(axis_r)], weight = 'bold', fontname = 'Gill Sans MT')
          if self.xlabel[str(axis_r)] != 'none':
            self.ax[axis_r].set_xlabel(self.xlabel[str(axis_r)], fontsize = self.xlabelsize[str(axis_r)], weight = 'bold', fontname = 'Gill Sans MT')
      
          #Set plot legend  
          if len(self.legend_elements[str(axis_r)]) > 0:
            if self.legend_title[str(axis_r)] == 'none':
              self.ax[axis_r].legend(handles = self.legend_elements[str(axis_r)], loc = self.legend_location[str(axis_r)], ncol = self.legend_columns[str(axis_r)], prop={'family':'Gill Sans MT','weight':'bold','size':self.legend_fontsize[str(axis_r)]}) 
            else:
              self.ax[axis_r].legend(handles = self.legend_elements[str(axis_r)], loc = self.legend_location[str(axis_r)], ncol = self.legend_columns[str(axis_r)], title=self.legend_title[str(axis_r)], title_fontsize = self.legend_title_fontsize[str(axis_r)], prop={'family':'Gill Sans MT','weight':'bold','size':self.legend_fontsize[str(axis_r)]}) 

    else:
      for axis_r in range(0, self.sub_rows):
        for axis_c in range(0, self.sub_cols):
          if self.sub_rows == 1:
            if len(self.xlim[str(axis_r)][str(axis_c)]) > 0:
              self.ax[axis_c].set_xlim(self.xlim[str(axis_r)][str(axis_c)])
            if len(self.ylim[str(axis_r)][str(axis_c)]) > 0:
              self.ax[axis_c].set_ylim(self.ylim[str(axis_r)][str(axis_c)])
      
          #Set axis ticks
            if self.xticks[str(axis_r)][str(axis_c)] == 'remove':
              self.ax[axis_c].set_xticks([])
              self.ax[axis_c].set_xticklabels('')
            else:
              if len(self.xtick_locations[str(axis_r)][str(axis_c)]) > 0:
                self.ax[axis_c].set_xticks(self.xtick_locations[str(axis_r)][str(axis_c)])
              if len(self.xtick_labels[str(axis_r)][str(axis_c)]) > 0:
                self.ax[axis_c].set_xticklabels(self.xtick_labels[str(axis_r)][str(axis_c)])
            if self.yticks[str(axis_r)][str(axis_c)] == 'remove':
              self.ax[axis_c].set_yticks([])
              self.ax[axis_c].set_yticklabels('')
            else:
              if len(self.ytick_locations[str(axis_r)][str(axis_c)]) > 0:
                self.ax[axis_c].set_yticks(self.ytick_locations[str(axis_r)][str(axis_c)])
              if len(self.ytick_labels[str(axis_r)][str(axis_c)]) > 0:
                self.ax[axis_c].set_yticklabels(self.ytick_labels[str(axis_r)][str(axis_c)])
            for tick in self.ax[axis_c].get_xticklabels():
              if self.tickfont[str(axis_r)][str(axis_c)] != 'none':
                tick.set_fontname(self.tickfont[str(axis_r)][str(axis_c)])
              if self.tickfontsize[str(axis_r)][str(axis_c)] > 0:
                tick.set_fontsize(self.tickfontsize[str(axis_r)][str(axis_c)])
            for tick in self.ax[axis_c].get_yticklabels():
              if self.tickfont[str(axis_r)][str(axis_c)] != 'none':
                tick.set_fontname(self.tickfont[str(axis_r)][str(axis_c)])
              if self.tickfontsize[str(axis_r)][str(axis_c)] > 0:
                tick.set_fontsize(self.tickfontsize[str(axis_r)][str(axis_c)])
        
            #Set axis labels
            if self.ylabel[str(axis_r)][str(axis_c)] != 'none':
              self.ax[axis_c].set_ylabel(self.ylabel[str(axis_r)][str(axis_c)], fontsize = self.ylabelsize[str(axis_r)][str(axis_c)], weight = 'bold', fontname = 'Gill Sans MT')
            if self.xlabel[str(axis_r)][str(axis_c)] != 'none':
              self.ax[axis_c].set_xlabel(self.xlabel[str(axis_r)][str(axis_c)], fontsize = self.xlabelsize[str(axis_r)][str(axis_c)], weight = 'bold', fontname = 'Gill Sans MT')
      
            #Set plot legend  
            if len(self.legend_elements[str(axis_r)][str(axis_c)]) > 0:
              if self.legend_title[str(axis_r)][str(axis_c)] == 'none':
                self.ax[axis_c].legend(handles = self.legend_elements[str(axis_r)][str(axis_c)], loc = self.legend_location[str(axis_r)][str(axis_c)], ncol = self.legend_columns[str(axis_r)][str(axis_c)], prop={'family':'Gill Sans MT','weight':'bold','size':self.legend_fontsize[str(axis_r)][str(axis_c)]}) 
              else:
                self.ax[axis_c].legend(handles = self.legend_elements[str(axis_r)][str(axis_c)], loc = self.legend_location[str(axis_r)][str(axis_c)], ncol = self.legend_columns[str(axis_r)][str(axis_c)], title=self.legend_title[str(axis_r)][str(axis_c)], title_fontsize = self.legend_title_fontsize[str(axis_r)][str(axis_c)], prop={'family':'Gill Sans MT','weight':'bold','size':self.legend_fontsize[str(axis_r)]}[str(axis_c)]) 
          else:
            if len(self.xlim[str(axis_r)][str(axis_c)]) > 0:
              self.ax[axis_r][axis_c].set_xlim(self.xlim[str(axis_r)][str(axis_c)])
            if len(self.ylim[str(axis_r)][str(axis_c)]) > 0:
              self.ax[axis_r][axis_c].set_ylim(self.ylim[str(axis_r)][str(axis_c)])
      
          #Set axis ticks
            if self.xticks[str(axis_r)][str(axis_c)] == 'remove':
              self.ax[axis_r][axis_c].set_xticks([])
              self.ax[axis_r][axis_c].set_xticklabels('')
            else:
              if len(self.xtick_locations[str(axis_r)][str(axis_c)]) > 0:
                self.ax[axis_r][axis_c].set_xticks(self.xtick_locations[str(axis_r)][str(axis_c)])
              if len(self.xtick_labels[str(axis_r)][str(axis_c)]) > 0:
                self.ax[axis_r][axis_c].set_xticklabels(self.xtick_labels[str(axis_r)][str(axis_c)])
            if self.yticks[str(axis_r)][str(axis_c)] == 'remove':
              self.ax[axis_r][axis_c].set_yticks([])
              self.ax[axis_r][axis_c].set_yticklabels('')
            else:
              if len(self.ytick_locations[str(axis_r)][str(axis_c)]) > 0:
                self.ax[axis_r][axis_c].set_yticks(self.ytick_locations[str(axis_r)][str(axis_c)])
              if len(self.ytick_labels[str(axis_r)][str(axis_c)]) > 0:
                self.ax[axis_r][axis_c].set_yticklabels(self.ytick_labels[str(axis_r)][str(axis_c)])
            for tick in self.ax[axis_r][axis_c].get_xticklabels():
              if self.tickfont[str(axis_r)][str(axis_c)] != 'none':
                tick.set_fontname(self.tickfont[str(axis_r)][str(axis_c)])
              if self.tickfontsize[str(axis_r)][str(axis_c)] > 0:
                tick.set_fontsize(self.tickfontsize[str(axis_r)][str(axis_c)])
            for tick in self.ax[axis_r][axis_c].get_yticklabels():
              if self.tickfont[str(axis_r)][str(axis_c)] != 'none':
                tick.set_fontname(self.tickfont[str(axis_r)][str(axis_c)])
              if self.tickfontsize[str(axis_r)][str(axis_c)] > 0:
                tick.set_fontsize(self.tickfontsize[str(axis_r)][str(axis_c)])
        
            #Set axis labels
            if self.ylabel[str(axis_r)][str(axis_c)] != 'none':
              self.ax[axis_r][axis_c].set_ylabel(self.ylabel[str(axis_r)][str(axis_c)], fontsize = self.ylabelsize[str(axis_r)][str(axis_c)], weight = 'bold', fontname = 'Gill Sans MT')
            if self.xlabel[str(axis_r)][str(axis_c)] != 'none':
              self.ax[axis_r][axis_c].set_xlabel(self.xlabel[str(axis_r)][str(axis_c)], fontsize = self.xlabelsize[str(axis_r)][str(axis_c)], weight = 'bold', fontname = 'Gill Sans MT')
      
            #Set plot legend  
            if len(self.legend_elements[str(axis_r)][str(axis_c)]) > 0:
              if self.legend_title[str(axis_r)][str(axis_c)] == 'none':
                self.ax[axis_r][axis_c].legend(handles = self.legend_elements[str(axis_r)][str(axis_c)], loc = self.legend_location[str(axis_r)][str(axis_c)], ncol = self.legend_columns[str(axis_r)][str(axis_c)], prop={'family':'Gill Sans MT','weight':'bold','size':self.legend_fontsize[str(axis_r)][str(axis_c)]}) 
              else:
                self.ax[axis_r][axis_c].legend(handles = self.legend_elements[str(axis_r)][str(axis_c)], loc = self.legend_location[str(axis_r)][str(axis_c)], ncol = self.legend_columns[str(axis_r)][str(axis_c)], title=self.legend_title[str(axis_r)][str(axis_c)], title_fontsize = self.legend_title_fontsize[str(axis_r)][str(axis_c)], prop={'family':'Gill Sans MT','weight':'bold','size':self.legend_fontsize[str(axis_r)]}[str(axis_c)]) 
    if use_tight_layout:
      plt.tight_layout()
    print('Printing: ' + self.filename)
    plt.savefig(figure_folder + self.filename + '.' + file_type, format = file_type, dpi = 300, bbox_inches = 'tight', pad_inches = 0.1)
    if show_plots:
      plt.show()
    plt.close()


  def plot_environmental_baseflow_as_pct_of_flow(self, all_contractors, flow_values, eflows_values, flow_res, start_year, current_year, output_folder):
    qalycolors = sns.color_palette('Blues', 100)
    monthly_flow = np.zeros(12*(current_year - start_year + 1))
    month_num = 10
    year_num = start_year - 1
    for index, row in flow_values.iterrows():
      if index.month > 9:
        month_num = index.month - 10
        year_num = index.year - (start_year - 1)
      else:
        month_num = index.month + 2
        year_num = index.year - start_year
      
      monthly_flow[month_num + year_num*12] += row[flow_res + '_inf'] * 1.98/1000.0

    for x in range(4, 0,-1):
      total_flow = monthly_flow * float(x) / 10.0
      self.ax.fill_between(all_contractors['date_index'], total_flow, color = qalycolors[x*25-1])
    
    environmental_baseflows = pd.DataFrame(index = all_contractors['date_index'], columns = ['Ecosystem Water Quality flows, GG et al', 'Full Modelled E-Baseflows', 'Modelled E-Baseflows, Shasta Demands'])
    environmental_baseflows['Full Modelled E-Baseflows'] = all_contractors['all_environmental_timeseries'] * 1000.0
    environmental_baseflows['Modelled E-Baseflows, Shasta Demands'] = all_contractors['environmental_timeseries'] * 1000.0
    for index, row in eflows_values.iterrows():
      environmental_baseflows.loc[index, 'Ecosystem Water Quality flows, GG et al'] = row['Net Ecosystem Water Quality and Flows']

    self.ax.plot(all_contractors['date_index'], all_contractors['all_environmental_timeseries'] * 1000.0, color = 'crimson', linewidth = 2.5)

    self.legend_elements = []
    for x_cnt, x in enumerate(['10%', '20%', '30%', '40%']):
      self.legend_elements.append(Patch(color = qalycolors[(x_cnt+1)*25-1], label = x + ' Inflows'))
    self.legend_elements.append(Line2D([0], [0], lw=2, color = 'crimson', label = 'Environmental baseflows'))
    self.legend_columns = 3
    self.legend_fontsize = 12
    self.xlim = [all_contractors['date_index'][0], all_contractors['date_index'][-1]]
    self.ylim = [0, max(np.max(monthly_flow) * 0.45, np.max(all_contractors['all_environmental_timeseries']) * 1200.0)]
    self.ylabel = 'Total flow (taf/month)'
    
  def plot_environmental_flow_types(self, all_contractors, fish_timeseries, start_year, current_year, output_folder):
    priority_labels = ['spring recession', 'winter peak', 'fall pulse']
    qalycolors = sns.color_palette('Blues', 100)
    qalycolors2 = sns.color_palette('Greens', 100)
  
    self.ax.fill_between(all_contractors['date_index'], np.zeros(len(all_contractors['environmental_timeseries'])), all_contractors['environmental_timeseries'] * 1000.0, facecolor = qalycolors2[24], linewidth = 0.5)
    cumulative_fill = np.zeros(len(all_contractors['environmental_timeseries']))

    all_environmental_flows = pd.DataFrame(index = all_contractors['date_index'][:(current_year - start_year)*12])
    all_environmental_flows['environmental_base'] = all_contractors['environmental_timeseries'][:(current_year - start_year)*12] * 1000.0
    all_other_flows = pd.DataFrame(index = np.arange(start_year, current_year))
    for x_cnt, x in enumerate(fish_timeseries):
      self.ax.fill_between(all_contractors['date_index'], all_contractors['environmental_timeseries'] * 1000.0, fish_timeseries[x] + all_contractors['environmental_timeseries'] * 1000.0, where=fish_timeseries[x]>=cumulative_fill, color = qalycolors2[(x_cnt+2)*25-1], interpolate=True)
      cumulative_fill += fish_timeseries[x]
      all_environmental_flows[priority_labels[x_cnt]] = fish_timeseries[x][:(current_year - start_year)*12]
    
    self.legend_elements = []
    for x_cnt, x in enumerate(['1 \n(Environmental Baseflows)', '2 \n(Spring Recession)', '3 \n(Winter Peak)', '4 \n(Fall Pulse)']):
      self.legend_elements.append(Patch(color = qalycolors2[(x_cnt+1)*25-1], label = 'Priority ' + x))
    self.legend_columns = 4
    self.legend_fontsize = 12

    #plot touch-ups
    self.xlim = [all_contractors['date_index'][0], all_contractors['date_index'][-1]]
    self.ylim = [0.0, np.max(all_contractors['environmental_timeseries'] * 1000.0 + cumulative_fill)*1.25]
    self.ylabel = 'Total Flow (taf/month)'


  def plot_total_demand_by_wyt(self, water_group_types, wyt_cats, all_contractors_wyt, new_demands, plot_type, output_folder):
    color_list = ['steelblue', 'teal', 'beige', 'indianred', 'maroon']
    column_mult = 6
  
    if plot_type == 'observed':
      self.ylim = [0, 4.5]
      for grp_cnt, grp in enumerate(water_group_types):
        self.xtick_locations.append(float(grp_cnt * column_mult) + 2.5)
        for wyt_cnt, wyt in enumerate(wyt_cats):
          self.ax.fill_between([wyt_cnt + grp_cnt*column_mult, wyt_cnt + 1 + grp_cnt*column_mult], [np.min(all_contractors_wyt[grp][wyt]), np.min(all_contractors_wyt[grp][wyt])], [np.max(all_contractors_wyt[grp][wyt]), np.max(all_contractors_wyt[grp][wyt])], color = color_list[wyt_cnt])
    elif plot_type == 'stylized':
      ordered_list = ['In-Basin', 'Exports', 'Salinity', 'Refuges']
      self.ylim = [0, 1.5]
      for grp_cnt, grp in enumerate(ordered_list):
        self.xtick_locations.append(float(grp_cnt * column_mult) + 2.5)
        self.xtick_labels.append(grp)
        for wyt_cnt, wyt in enumerate(wyt_cats):
          self.ax.fill_between([wyt_cnt + grp_cnt*column_mult, wyt_cnt + 1 + grp_cnt*column_mult], [0.0, 0.0], [new_demands[grp][wyt], new_demands[grp][wyt]], color = color_list[wyt_cnt])
      
    for wyt_cnt, wyt in enumerate(['W', 'AN', 'BN', 'D', 'C']):
      self.legend_elements.append(Patch(facecolor = color_list[wyt_cnt], edgecolor = 'black', label = wyt))
        
    if plot_type == 'observed':
      self.xtick_labels = ['Junior\nin-basin', 'Senior\nin-basin', 'Salinty','Riparian', 'Exports', 'Refuges', 'Envrio', 'Cold\nPool', 'Flood\nReleases']
    #self.xlim = [all_contractors['date_index'][0], all_contractors['date_index'][-1]]
    self.ylabel = 'Total Consumption (mAF)'
    self.ylabelsize = 20
    self.tickfontsize = 16
    self.legend_fontsize = 16
    self.legend_location = 'upper right'
  def make_storage_allocation_block(self, user_class, user_groups, label_names, cold_pool_storage, class_2_total, cold_pool_category, environmental_category, use_class_2, output_folder):
    color_list = ['navy', 'steelblue', 'teal', 'olive', 'goldenrod', 'indianred', 'maroon']
    start_position = 0.0
    start_position2 = 0.0
    storage_class_1 = 4.552 - cold_pool_storage
    for ug_cnt, ug in enumerate(user_groups):
      if ug == cold_pool_category:
        self.ax.fill_between([0.0, 1.0], [0.0, 0.0], [cold_pool_storage, cold_pool_storage], color = 'beige', alpha = 1.0)
        self.ax.fill_between([0.0, 1.0], [0.0, 0.0], [cold_pool_storage, cold_pool_storage], color = color_list[ug_cnt], alpha = 0.5)
        self.ax.text(0.5, cold_pool_storage/2.0, label_names[ug_cnt], fontsize = 18, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='center',
            horizontalalignment='center', zorder = 20)
      else:
        self.ax.fill_between([start_position, start_position + user_class[ug]['class_1_portion']], [cold_pool_storage, cold_pool_storage], [cold_pool_storage + storage_class_1, cold_pool_storage + storage_class_1], color = 'beige', alpha = 1.0)
        self.ax.fill_between([start_position, start_position + user_class[ug]['class_1_portion']], [cold_pool_storage, cold_pool_storage], [cold_pool_storage + storage_class_1, cold_pool_storage + storage_class_1], color = color_list[ug_cnt], alpha = 0.5)
        if ug == environmental_category:
          line_placement = start_position * 1.0
        if user_class[ug]['class_1_portion'] > 0.1:
          self.ax.text(start_position + user_class[ug]['class_1_portion']/2.0, cold_pool_storage + storage_class_1/2.0, label_names[ug_cnt], fontsize = 18, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='center',
              horizontalalignment='center', zorder = 20)
        elif user_class[ug]['class_1_portion'] > 0.0:
          self.ax.text(start_position + user_class[ug]['class_1_portion']/2.0, cold_pool_storage + storage_class_1/2.0, label_names[ug_cnt], fontsize = 18, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='center',
              horizontalalignment='center', zorder = 20, rotation = 90)
            
        if use_class_2:
          modify_figure = True
          if modify_figure:
            if ug != environmental_category and user_class[ug]['class_2_portion'] > 0.0:
              self.ax.fill_between([0.0, 1.0], [cold_pool_storage + storage_class_1, cold_pool_storage + storage_class_1],[cold_pool_storage + storage_class_1 + class_2_total, cold_pool_storage + storage_class_1 + class_2_total],color = 'beige', alpha = 1.0)
              self.ax.fill_between([0.0, 1.0], [cold_pool_storage + storage_class_1, cold_pool_storage + storage_class_1],[cold_pool_storage + storage_class_1 + class_2_total, cold_pool_storage + storage_class_1 + class_2_total], color = color_list[ug_cnt], alpha = 0.5)
              self.ax.text(0.5, cold_pool_storage + storage_class_1 + class_2_total/2.0, label_names[ug_cnt], fontsize = 18, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='center', horizontalalignment='center', zorder = 20)
          else:
            self.ax.fill_between([start_position2, start_position2 + user_class[ug]['class_2_portion']], [cold_pool_storage + storage_class_1, cold_pool_storage + storage_class_1], [cold_pool_storage + storage_class_1 + class_2_total, cold_pool_storage + storage_class_1 + class_2_total],color = 'beige', alpha = 1.0)
            self.ax.fill_between([start_position2, start_position2 + user_class[ug]['class_2_portion']], [cold_pool_storage + storage_class_1, cold_pool_storage + storage_class_1],[cold_pool_storage + storage_class_1 + class_2_total, cold_pool_storage + storage_class_1 + class_2_total], color = color_list[ug_cnt], alpha = 0.5)
            if user_class[ug]['class_2_portion'] > 0.1:
              self.ax.text(start_position2 + user_class[ug]['class_2_portion']/2.0, cold_pool_storage + storage_class_1 + class_2_total/2.0, label_names[ug_cnt], fontsize = 18, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='center',
                horizontalalignment='center', zorder = 20)
            elif user_class[ug]['class_2_portion'] > 0.0:
              self.ax.text(start_position2 + user_class[ug]['class_2_portion']/2.0, cold_pool_storage + storage_class_1 + class_2_total/2.0, label_names[ug_cnt], fontsize = 18, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='center',
                horizontalalignment='center', zorder = 20, rotation = 90)

      start_position+=user_class[ug]['class_1_portion']
      start_position2+=user_class[ug]['class_2_portion']
      
    self.xlim = [0.0, 1.0]
    self.xlabel = 'Storage Allocation'
    self.xlabelsize = 20
    self.xtick_locations = [0.0, 0.25, 0.5, 0.75, 1.0]
    self.xtick_labels = ['0%','25%','50%','75%','100%']

    if use_class_2:
      self.ylim = [0.0, cold_pool_storage + storage_class_1 + class_2_total]
      self.ytick_locations = [cold_pool_storage, cold_pool_storage + storage_class_1, cold_pool_storage + storage_class_1 + class_2_total]
      self.ytick_labels = [str(float(int(cold_pool_storage * 100))/100), str(float(int((cold_pool_storage + storage_class_1) * 100))/100), '']
      self.ylabel = 'Allocated Storage (maf)'
      self.ylabelsize = 20
      self.ax.plot([0.0, 1.0], [cold_pool_storage, cold_pool_storage], color = 'black', linewidth = 2.0)
      self.ax.plot([0.0, 1.0], [cold_pool_storage + storage_class_1 + class_2_total, cold_pool_storage + storage_class_1 + class_2_total], color = 'black', linewidth = 2.0)
      self.ax.plot([0.0, 1.0], [0.0, 0.0], color = 'black', linewidth = 2.0)
      self.ax.plot([0.0, 1.0], [cold_pool_storage + storage_class_1-0.01, cold_pool_storage + storage_class_1-0.01], color = 'black', linewidth = 2.0)
      self.ax.plot([line_placement, line_placement], [cold_pool_storage, cold_pool_storage + storage_class_1], color = 'black', linewidth = 2.0)
    else:
      self.ylim = [0.0, cold_pool_storage + storage_class_1]
      self.yticks = 'remove'      
    self.tickfontsize = 24

  def plot_timeseries_allocations(self, datetime_index, total_storage, environmental_flow_portion_int, output_folder):
    color_list = ['teal', 'beige', 'indianred', 'maroon']
    self.ax.fill_between(datetime_index, total_storage['storage'], color='beige', alpha = 1.0)
    self.ax.fill_between(datetime_index, total_storage['storage'], color='steelblue', alpha = float(environmental_flow_portion_int) / 5.0)
    self.ylim = [1, 5]
    self.ylabel = 'Reservoir Storage\n(mAF)'
    self.ylabelsize = 18
    self.xticks = 'remove'
    self.xlim = [datetime_index[1], datetime_index[-1]]
    self.legend_elements = []
    for x_cnt, x in enumerate(['10%', '20%', '30%', '40%']):
      self.legend_elements.append(Patch(facecolor = 'steelblue', edgecolor = 'black', alpha = float(x_cnt+1)/5.0, label = x))
    self.legend_columns = 5
    self.legend_title = "Flow/Storage Portion for Environment"
    self.tickfontsize = 16
    
  def plot_shortfall_tradeoffs(self, num_lines, output_folder):

    color_list = sns.color_palette('RdBu', 4)
    user_groups = ['Cold-Pool', 'Salinity', 'In-Basin', 'Exports', 'Refuges', 'Environment_class1', 'Environment_class2']
    pass_through_scenarios = ['pass_through_0','pass_through_1250']
    ewb_scenarios = ['EWB_0','EWB_1250']
    if num_lines == 2:
      zip_colors = [0, 1]
      zip_names = [pass_through_scenarios[0],pass_through_scenarios[1]]
      legend_labels = ['EWB with pass through flows', 'EWB with pass through flows +\n1.25 MAF minimum storage']
    elif num_lines == 3:
      zip_colors = [0, 2, 3]
      zip_names = [pass_through_scenarios[0], ewb_scenarios[0], ewb_scenarios[1]]
      legend_labels = ['EWB with pass through flows', 'EWB with storage', 'EWB with storage + 1.25 MAF minimum storage']
    elif num_lines == 4:
      zip_colors = [0, 1, 2, 3]
      zip_names = [pass_through_scenarios[0], pass_through_scenarios[1], ewb_scenarios[0], ewb_scenarios[1]]
      legend_labels = ['EWB with pass through flows', 'EWB with pass through flows +\n1.25 MAF minimum storage', 'EWB with storage', 'EWB with storage +\n1.25 MAF minimum storage']
      
    for sce_cnt, simplified_scenario in zip(zip_colors, zip_names):
      simplified_shortfalls = pd.read_csv(output_folder + 'simplified_shortfalls_' + simplified_scenario + '_with_storage_0.csv')
      self.ax.plot(simplified_shortfalls['eco'], simplified_shortfalls['other'], color = color_list[sce_cnt], marker = 'o', markeredgewidth = 3, markeredgecolor='black', markerfacecolor = color_list[sce_cnt], markersize = 25, lw=3.0)

      if simplified_scenario == ewb_scenarios[1]:
        plot_labels = ['10%', '20%', '30%', '40% (EWB inflow allocation)']
      else:
        plot_labels = ['10%', '20%', '30%', '40%']

      for x in range(0, 4):
        if simplified_scenario == ewb_scenarios[1] or simplified_scenario == pass_through_scenarios[1]:
          if x == 3 and simplified_scenario == 'EWB_0':
            self.ax.text(simplified_shortfalls['eco'][x], simplified_shortfalls['other'][x] + 1.5, plot_labels[x], fontsize = 19, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='bottom',
                  horizontalalignment='center', zorder = 20)
          elif x == 1 and simplified_scenario == 'EWB_1250':
            self.ax.text(simplified_shortfalls['eco'][x], simplified_shortfalls['other'][x] + 1.5, plot_labels[x], fontsize = 19, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='bottom',
                  horizontalalignment='center', zorder = 20)
          else:
            if plot_labels[x] == '40% (EWB inflow allocation)':          
              self.ax.text(simplified_shortfalls['eco'][x] + 1.0, simplified_shortfalls['other'][x] + 1.0, plot_labels[x], fontsize = 22, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='bottom',
                  horizontalalignment='left', zorder = 20)
            else:
              self.ax.text(simplified_shortfalls['eco'][x] + 1.0, simplified_shortfalls['other'][x] + 1.0, plot_labels[x], fontsize = 19, weight = 'bold', fontname = 'Gill Sans MT',verticalalignment='bottom',
                  horizontalalignment='left', zorder = 20)

    self.legend_fontsize = 28
    self.tickfontsize = 22
    self.ylabelsize = 24
    self.xlabelsize = 24
    self.xlim = [-1.5, 75.0]
    self.ylim = [-1.5, 75.0]
    self.ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals = 0))
    self.ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals = 0))
    self.legend_elements = []
    for x_cnt, x in zip(zip_colors, legend_labels):
      self.legend_elements.append(Circle((0,0), facecolor = color_list[x_cnt], edgecolor = 'black', label = x))
    self.legend_location = 'upper right'
    self.xlabel = 'Shortfall in EWB demands (%)\n(Baseflow, Functional Flow)'
    self.ylabel = 'Shortfall in demands with existing priority (%)\n(In-Basin, System, Refuges, Exports)'
    
    
  def plot_temperature_attainment(self, output_folder):
    temp_attainment = pd.read_csv(output_folder + 'temp_priorities_non-attainment_6-6-22.csv')
    temp_attainment2 = pd.read_csv(output_folder + 'temp_priorities_non-attainment_5-26-22.csv')

    color_list = sns.color_palette('gist_earth_r', 4)
    fig_group_list = ['Primary\nno storage', 'Secondary\nno storage', 'Primary\nw/storage', 'Secondary\nw/storage']
    label_name_use = []
    label_location_use = []
    use_list = ['PT', 'EWB']
    min_list = ['0', '1250']
    req_list = ['Primary', 'Secondary']
    cold_pool_loc = 0
    plot_counter = 0
    for use_cnt, use_type in enumerate(use_list):
      for min_cnt, min_type in enumerate(min_list):
        for temp_cnt, temp_req in enumerate(req_list):
          plotting_values = np.zeros(4)
          starting_loc = 0
          if temp_req == 'Secondary':
            starting_loc += 4
          if use_type == 'PT':
            starting_loc += 8
          for x in range(0,4):
            if use_type == 'PT' and min_type == '0':
              plotting_values[x] += temp_attainment.loc[starting_loc + x, 'AvgAnn_months_non-attainment']
            elif use_type == 'PT' or min_type == '0':
              plotting_values[x] += temp_attainment2.loc[starting_loc + x, 'AvgAnn_months_non-attainment']
            else:
              plotting_values[x] += temp_attainment.loc[starting_loc + x, 'AvgAnn_months_non-attainment']
      
          if temp_req == 'Primary':
            use_loc = 0
          else:
            use_loc = 5    
          for x in range(0, 4):
            if min_type == '0':
              alpha_use = 0.5
            elif min_type == '1250':
              alpha_use = 1.0        
            self.ax[plot_counter].fill_between([use_loc + x, use_loc + 1 +x], [0.0, 0.0], [plotting_values[x], plotting_values[x]], facecolor = 'beige', alpha = 1.0, linewidth = 0.0)
            self.ax[plot_counter].fill_between([use_loc + x, use_loc + 1 +x], [0.0, 0.0], [plotting_values[x], plotting_values[x]], facecolor = color_list[x], edgecolor = 'black', linewidth = 1.0, alpha = alpha_use)
      
      plot_counter += 1
      
    self.xticks['0'] = 'remove'
    self.ylabel['0'] = 'Annual months of non-attainment\npass-through allocation'
    self.ylabel['1'] = 'Annual months of non-attainment\nEWB storage allocation'
    self.xtick_locations['1'] = [2, 7]
    self.xtick_labels['1'] = ['Primary temperature objectives', 'Secondary temperature objectives']
    for axis_use in ['0', '1']:
      self.tickfontsize[axis_use] = 22
      self.ylabelsize[axis_use] = 18
      self.ylim[axis_use] = [0, 5.0]
    self.legend_elements['0'] = []
    for x_cnt, x in enumerate(['10% allocation', '20% allocation', '30% allocation', '40% allocation']):
      self.legend_elements['0'].append(Patch(facecolor = color_list[x_cnt], edgecolor = 'black', alpha = 1.0, label = x))
    for x_cnt, x in enumerate(['No minimum', '1.25 maf minimum storage']):
      self.legend_elements['0'].append(Patch(facecolor = 'black', edgecolor = 'black', alpha = float(x_cnt + 1)/2.0, label = x))
    self.legend_columns['0'] = 3

  def plot_shortage_bar_charts(self, storage_type, output_folder):
    if storage_type == 'EWB':
      shortfalls_0 = pd.read_csv(output_folder + 'shortfalls_by_wyt_' + storage_type + '_0_with_storage_0.csv')
      shortfalls_1250 = pd.read_csv(output_folder + 'shortfalls_by_wyt_' + storage_type + '_1250_with_storage_0.csv')
      shortfalls_1000 = pd.read_csv(output_folder + 'shortfalls_by_wyt_' + storage_type + '_1000_with_storage_0.csv')
      shortfalls_1500 = pd.read_csv(output_folder + 'shortfalls_by_wyt_' + storage_type + '_1500_with_storage_0.csv')
    elif storage_type == 'all':
      shortfalls_pt_0 = pd.read_csv(output_folder + 'shortfalls_by_wyt_pass_through_0_with_storage_0.csv')
      shortfalls_pt_1250 = pd.read_csv(output_folder + 'shortfalls_by_wyt_pass_through_1250_with_storage_0.csv')
      shortfalls_0 = pd.read_csv(output_folder + 'shortfalls_by_wyt_EWB_0_with_storage_0.csv')
      shortfalls_1250 = pd.read_csv(output_folder + 'shortfalls_by_wyt_EWB_1250_with_storage_0.csv')
    else:
      shortfalls_0 = pd.read_csv(output_folder + 'shortfalls_by_wyt_' + storage_type + '_0_with_storage_0.csv')
      shortfalls_1250 = pd.read_csv(output_folder + 'shortfalls_by_wyt_' + storage_type + '_1250_with_storage_0.csv')
    
    color_list = ['steelblue', 'teal', 'goldenrod', 'indianred', 'maroon', 'indigo']
    fig_group_list = ['junior', 'senior', 'export', 'refuge', 'delta', 'environmental']
    use_list = ['Cold-Pool', 'Salinity', 'In-Basin', 'Refuges', 'Exports', 'Environment_class1', 'Environment_class2']
    label_names = ['Cold-Pool', 'System', 'In-Basin',  'Refuges', 'Exports', 'Environmental\nBaseflows', 'Functional\nFlows']
    for wyt_cnt, wyt in enumerate(['W', 'AN', 'BN', 'D', 'C']):
      for uc_cnt, uc in enumerate(use_list):
        if uc != 'Cold-Pool':
          for env_range in range(1, 5):
            if uc == 'Environment_class1' or uc == 'Environment_class2':
              env_count = env_range * 1
            else:
              env_count = 5 - env_range
            environmental_flow_portion = float(5 - env_count) / 5.0
            shortage_amount0 = shortfalls_0.loc[env_count-1, uc + '_' + wyt]* 100
            shortage_amount1 = shortfalls_1250.loc[env_count-1, uc + '_' + wyt] * 100
            if storage_type == 'EWB':
              shortage_amount2 = shortfalls_1000.loc[env_count-1, uc + '_' + wyt]* 100
              shortage_amount3 = shortfalls_1500.loc[env_count-1, uc + '_' + wyt] * 100
              self.ax[0].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount0, shortage_amount0], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[0].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount0, shortage_amount0], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
              self.ax[1].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount2, shortage_amount2], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[1].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount2, shortage_amount2], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
              self.ax[2].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount1, shortage_amount1], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[2].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount1, shortage_amount1], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
              self.ax[3].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount3, shortage_amount3], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[3].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount3, shortage_amount3], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
            elif storage_type == 'all':
              shortage_amount_pt0 = shortfalls_pt_0.loc[env_count-1, uc + '_' + wyt]* 100
              shortage_amount_pt1 = shortfalls_pt_1250.loc[env_count-1, uc + '_' + wyt] * 100
              self.ax[0].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount_pt0, shortage_amount_pt0], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[0].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount_pt0, shortage_amount_pt0], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
              self.ax[1].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount_pt1, shortage_amount_pt1], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[1].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount_pt1, shortage_amount_pt1], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
              self.ax[2].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount0, shortage_amount0], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[2].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount0, shortage_amount0], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
              self.ax[3].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount1, shortage_amount1], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[3].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount1, shortage_amount1], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
            else:
              self.ax[0].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount0, shortage_amount0], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[0].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount0, shortage_amount0], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
              self.ax[1].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount1, shortage_amount1], color = 'beige', alpha = 1.0, linewidth = 0.0)
              self.ax[1].fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [shortage_amount1, shortage_amount1], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
    
    for axis_no, label_words1, label_words2, label_words3 in zip(['0', '1', '2', '3'], ['no', '1.0 maf', '1.25 maf', '1.5 maf'], ['pass-through', 'pass_through', 'EWB storage', 'EWB storage'], ['no', '1.25 maf', 'no', '1.25 maf']):
      if storage_type == 'EWB':
        self.ylabel[axis_no] = 'Shortfall, % of annual demand\n' + label_words1 + ' minimum storage'
      elif storage_type == 'all':
        self.ylabel[axis_no] = 'Shortfall, % of annual demand\n' + label_words2 + ' allocation\n' + label_words3 + ' minimum storage'
    if storage_type == 'pass_through':
      self.ylabel['0'] = 'Shortfall, % of annual demand\nno minimum storage'
      self.ylabel['1'] = 'Shortfall, % of annual demand\n1.25 maf minimum storage'
    for axis_no in ['0', '1']:
      self.ylabelsize[axis_no] = 18
    if storage_type == 'all' or storage_type == 'EWB':
      for axis_no in ['2', '3']:
        self.ylabelsize[axis_no] = 18
      
    for axis_no in range(0, self.sub_rows):
      self.xticks[str(axis_no)] = 'remove'
      self.ylim[str(axis_no)] = [0, 100]
      self.tickfontsize[str(axis_no)] = 16
    if storage_type == 'EWB' or storage_type == 'all':
      label_axis = ['0', '1', '2', '3']
    else:
      label_axis = ['0', '1']
    for uc_cnt, uc in enumerate(use_list):
      if uc != 'Cold-Pool':
        for axis_no in label_axis:
          self.xtick_labels[axis_no].append(label_names[uc_cnt])
          self.xtick_locations[axis_no].append(2.5 + 6*uc_cnt)
          self.xticks[axis_no] = 'keep'
    for wyt_cnt, wyt in enumerate(['W', 'AN', 'BN', 'D', 'C']):
      self.legend_elements['0'].append(Patch(facecolor = color_list[wyt_cnt], edgecolor = 'black', label = wyt))
    for x_cnt, x in enumerate(['10%', '20%', '30%', '40%']):
      self.legend_elements['0'].append(Patch(facecolor = 'black', edgecolor = 'black', alpha = float(5-(x_cnt+1))/5.0, label = x))
    self.legend_columns['0'] = 2


  def plot_partial_shortage_tradeoff(self, plot_type, output_folder):
    shortfalls = pd.read_csv(output_folder + 'subgroup_demands_cold_pool_' + plot_type + '_with_storage_0.csv', index_col = 0)
    water_year_types = ['W', 'W', 'W', 'W', 'AN', 'D', 'D', 'AN', 'BN', 'AN', 'W', 'D', 'C', 'D', 'BN', 'W', 'BN', 'D', 'C', 'C', 'BN', 'W', 'BN', 'W', 'D', 'C']

    color_list = ['steelblue', 'teal', 'goldenrod', 'indianred', 'maroon', 'indigo']
    fig_group_list = ['junior', 'senior', 'export', 'refuge', 'delta', 'environmental']
    use_list = ['Salinity', 'In-Basin', 'Refuges', 'Exports']
    label_names = ['System', 'In-Basin',  'Refuges', 'Exports']

    total_demand = {}
    total_shortfall = {}
    for uc in use_list:
      total_demand[uc] = {}
      total_shortfall[uc] = {}
      for x in ['W', 'D']:
        total_demand[uc][x] = 0.0
        total_shortfall[uc][x] = np.zeros(4)
    for wyt_cnt, wyt in enumerate(water_year_types):
      for uc_cnt, uc in enumerate(use_list):
        if wyt == 'W' or wyt == 'AN':
          total_demand[uc]['W'] += shortfalls.loc[wyt_cnt, uc]
        else:
          total_demand[uc]['D'] += shortfalls.loc[wyt_cnt, uc]
    
        for env_range in range(1, 5):
          if wyt == 'W' or wyt == 'AN':
            total_shortfall[uc]['W'][env_range-1] += shortfalls.loc[wyt_cnt, uc]- shortfalls.loc[wyt_cnt, uc + '_' + str(int(10*env_range))]
          else:
            total_shortfall[uc]['D'][env_range-1] += shortfalls.loc[wyt_cnt, uc] - shortfalls.loc[wyt_cnt, uc + '_' + str(int(10*env_range))]
      
    for uc_cnt, uc in enumerate(use_list):
      self.ax[0].plot(100*total_shortfall[uc]['W'] / total_demand[uc]['W'], color = color_list[uc_cnt], linewidth = 3.0)
      self.ax[1].plot(100*total_shortfall[uc]['D'] / total_demand[uc]['D'], color = color_list[uc_cnt], linewidth = 3.0)
    for axis_no in range(0, 2):
      self.ax[0].set_ylabel('Previously allocated demands met, %', fontsize = 12, labelpad = 13,  fontname = 'Helvetica')
      self.ax[1].set_ylabel('Previously allocated demands met, %', fontsize = 12, labelpad = 13,  fontname = 'Helvetica')
      self.ax[0].set_xlabel('Proportion of inflow pass-through ', fontsize = 13,  fontname = 'Helvetica', labelpad = 13)
      self.ax[1].set_xlabel('Proportion of inflow pass-through ', fontsize = 13,  fontname = 'Helvetica', labelpad = 13)
      self.xlim['0'][str(axis_no)] = [-0.5, 3.5]
      self.ylim['0'][str(axis_no)] = [0.0, 100.0]
      self.tickfontsize['0'][str(axis_no)] = 12
      self.ax[axis_no].xaxis.set_ticks_position('none') 
      self.ax[axis_no].yaxis.set_ticks_position('none') 
      self.tickfont['0'][str(axis_no)] = 'none'

      for env_range in range(1, 5):
        self.xtick_labels['0'][str(axis_no)].append(str(int(env_range * 10)) + '%')
        self.xtick_locations['0'][str(axis_no)].append(env_range - 1)
      for xx in range(0, 11):
        self.ytick_labels['0'][str(axis_no)].append(xx * 10)
        self.ytick_locations['0'][str(axis_no)].append(xx * 10)
        
        
    self.ax[0].set_title('c) Average other water user objectives met in wet years',fontsize = 12, ha='left', x=-0.1675,y=1.0575, fontweight = 'bold')
    self.ax[1].set_title('d) Average other water user objectives met in dry years',fontsize = 12, ha='left', x=-0.155,y=1.0575, fontweight = 'bold')
    self.ax[1].plot([3.49, 3.49], [0,100], linewidth = 1.25, color = 'black')

    for ax_num in range(0, 2):
      for tick in self.ax[ax_num].get_yaxis().get_major_ticks():
        tick.set_pad(9.25)
      for tick in self.ax[ax_num].get_xaxis().get_major_ticks():
        tick.set_pad(7.5)

    legend_elements = []
    for uc_cnt, uc in enumerate(label_names):
      legend_elements.append(Line2D([0],[0], linewidth=3, color = color_list[uc_cnt], label = uc))
    self.ax[0].legend(handles = legend_elements, loc = 'lower left',  labelspacing = 1.25, prop={'weight':'bold','size':12})
    self.ax[1].legend(handles = legend_elements, loc = 'lower left',  labelspacing = 1.25, prop={'weight':'bold','size':12})

  def plot_storage_pass_through_flows(self, plot_type, output_folder):
    pass_through = pd.read_csv(output_folder + 'storage_allocations_' + plot_type + '_with_storage_0.csv', index_col = 0)
    datetime_index = pd.to_datetime(pass_through.index)
    qalycolors = sns.color_palette('Blues', 4)
    for env_num in range(1, 5):
      env_count = env_num
      self.ax.fill_between(datetime_index, pass_through['total_storage_' + str(10 * env_num)] / 1000.0, facecolor=qalycolors[env_num -1], alpha = 1.0)
    self.ax.plot(datetime_index, pass_through['total_storage_' + str(10)] / 1000.0, color = 'black', linewidth = 1.5, alpha = 1.0)
    self.ylim = [0.0, 5.3]
    self.ylabel = 'Total reservoir storage (maf)\n pass-through EWB allocation'
    self.ylabelsize = 24
    self.tickfontsize = 20

    self.xtick_locations = [datetime(2000, 1, 1, 0 ,0), datetime(2010, 1, 1, 0 ,0), datetime(2020, 1, 1, 0 ,0)]
    self.xtick_labels =['2000', '2010', '2020']
    self.xlim = [datetime_index[1], datetime_index[-1]]

    self.legend_elements = []
    for x_cnt, x in enumerate(['10%', '20%', '30%', '40%']):
      self.legend_elements.append(Patch(facecolor = qalycolors[x_cnt], edgecolor = 'black', label = x + ' inflow'))
    self.legend_columns = 4
    self.legend_fontsize = 20

  def plot_individual_storage_allocations(self, enviro_allocation, output_folder):
    color_list = sns.color_palette('viridis', 8)
    counter = 0
    for file_type, file_label in zip(['pass_through_0', 'pass_through_1250', 'EWB_0', 'EWB_1250'], ['No minimum\npass-through','1.25 maf minimum\npass-through','No minimum\nEWB storage','1.25 maf minimum\nEWB storage']):
      cold_pool = pd.read_csv(output_folder + 'individual_storage_allocations_' + file_type + '_with_storage_0.csv', index_col = 0)
      datetime_index = pd.to_datetime(cold_pool.index)
      baseline = np.zeros(len(datetime_index))
      counter2 = 0
      for uc_cnt, uc in enumerate(cold_pool):
        if uc[-1] == str(enviro_allocation):
          self.ax[counter].fill_between(datetime_index, baseline, baseline + cold_pool[uc], color = 'beige', edgecolor = 'none', linewidth = 0.0, alpha = 1.0)
          self.ax[counter].fill_between(datetime_index, baseline, baseline + cold_pool[uc], facecolor = color_list[counter2 + 1], edgecolor = color_list[counter2 + 1], alpha = 0.8)
          baseline+=cold_pool[uc]
          counter2 += 1
      self.ax[counter].plot(datetime_index,baseline, color = 'black', linewidth = 1.5, alpha = 1.0)
      self.xlim[str(counter)] = [datetime_index[0], datetime_index[-1]]
      self.ylim[str(counter)] = [0.0, 5.5]
      self.ylabel[str(counter)] = file_label 
      self.ylabelsize[str(counter)] = 24
      self.xticks[str(counter)] = 'remove'
      self.tickfontsize[str(counter)] = 20
      counter += 1
  
    self.xticks[str(counter-1)] = 'keep'
    self.xtick_locations[str(counter-1)] = [datetime(2000, 1, 1, 0 ,0), datetime(2010, 1, 1, 0 ,0), datetime(2020, 1, 1, 0 ,0)]
    self.xtick_labels[str(counter-1)] = ['2000', '2010', '2020']
    self.tickfontsize[str(counter-1)] = 20
        
    counter = 0
    for uc_cnt, uc in enumerate(cold_pool):
      if uc[-1] == str(enviro_allocation):
        if uc[:-2] != 'Environment' and uc[:-2] != 'Cold-Pool':
          self.legend_elements['0'].append(Patch(facecolor = color_list[counter + 1], edgecolor = 'black', label = uc[:-2], alpha = 1.0))
        if uc[:-2] != 'Environment':
          self.legend_elements['1'].append(Patch(facecolor = color_list[counter + 1], edgecolor = 'black', label = uc[:-2], alpha = 1.0))
        if uc[:-2] != 'Cold-Pool':
          if uc[:-2] == 'Environment':
            self.legend_elements['2'].append(Patch(facecolor = color_list[counter + 1], edgecolor = 'black', label = 'EWB', alpha = 1.0))
          else:
            self.legend_elements['2'].append(Patch(facecolor = color_list[counter + 1], edgecolor = 'black', label = uc[:-2], alpha = 1.0))
        if uc[:-2] == 'Environment':
          self.legend_elements['3'].append(Patch(facecolor = color_list[counter + 1], edgecolor = 'black', label = 'EWB', alpha = 1.0))
        else:
          self.legend_elements['3'].append(Patch(facecolor = color_list[counter + 1], edgecolor = 'black', label = uc[:-2], alpha = 1.0))
          
        counter += 1
        
    for x in range(0, self.sub_rows):
      self.legend_columns[str(x)] = 6
      if x < 2:
        self.legend_fontsize[str(x)] = 20
      else:
        self.legend_fontsize[str(x)] = 19.5


  def plot_shortage_with_off_site_storage(self, output_folder):
    off_storage = {}
    off_storage['none'] = pd.read_csv(output_folder + 'shortfalls_by_wyt_EWB_1250_with_storage_0.csv')
    off_storage['1taf'] = pd.read_csv(output_folder + 'shortfalls_by_wyt_EWB_1250_with_storage_500.csv')
    off_storage['2taf'] = pd.read_csv(output_folder + 'shortfalls_by_wyt_EWB_1250_with_storage_1000.csv')
    off_storage['5taf'] = pd.read_csv(output_folder + 'shortfalls_by_wyt_EWB_1250_with_storage_2500.csv')

    color_list = ['steelblue', 'teal', 'goldenrod', 'indianred', 'maroon', 'indigo']
    fig_group_list = ['junior', 'senior', 'export', 'refuge', 'delta', 'environmental']
    use_list = ['Cold-Pool', 'Salinity', 'In-Basin', 'Refuges', 'Exports', 'Environment_class1', 'Environment_class2']
    label_names = ['Cold-Pool', 'Salinity', 'In-Basin',  'Refuges', 'Exports', 'E-Base', 'E-Functional Flows']
    for wyt_cnt, wyt in enumerate(['W', 'AN', 'BN', 'D', 'C']):
      for uc_cnt, uc in enumerate(['none', '1taf', '2taf', '5taf']):
        for env_range in range(1, 5):
          env_count = env_range * 1
          environmental_flow_portion = float(5 - env_count) / 5.0
          total_missed = off_storage[uc].loc[env_count-1, 'Environment_class1_' + wyt]*100
          total_missed2 = off_storage[uc].loc[env_count-1, 'Environment_class2_' + wyt]*100
          self.ax.fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [total_missed, total_missed], color = 'beige', alpha = 1.0, linewidth = 0.0)
          self.ax.fill_between([wyt_cnt + uc_cnt*6, wyt_cnt + 1 + uc_cnt*6], [0.0, 0.0], [total_missed, total_missed], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
          self.ax.fill_between([wyt_cnt + 24 + uc_cnt*6, wyt_cnt + 25 + uc_cnt*6], [0.0, 0.0], [total_missed2, total_missed2], color = 'beige', alpha = 1.0, linewidth = 0.0)
          self.ax.fill_between([wyt_cnt + 24 + uc_cnt*6, wyt_cnt + 25 + uc_cnt*6], [0.0, 0.0], [total_missed2, total_missed2], color = color_list[wyt_cnt], alpha = environmental_flow_portion)
        
    self.xtick_locations = [2.5, 8.5, 14.5, 20.5, 26.5, 32.5, 38.5, 44.5]
    self.xtick_labels = ['Primary\nno downstream\nstorage', 'Primary\ndiversion\nto storage:\n500 CFS', 'Primary\ndiversion\nto storage:\n1000 CFS', 'Primary\ndiversion\nto storage:\n2500 CFS', 'Secondary\nno downstream\nstorage', 'Secondary\ndiversion\nto storage:\n500 CFS', 'Secondary\ndiversion\nto storage:\n1000 CFS', 'Secondary\ndiversion\nto storage:\n2500 CFS']
    self.ylabel = 'Annual ecosystem shortfall, % of demand'
    self.ylabelsize = 18
    self.ylim = [0, 100]

    for wyt_cnt, wyt in enumerate(['W', 'AN', 'BN', 'D', 'C']):
      self.legend_elements.append(Patch(facecolor = color_list[wyt_cnt], edgecolor = 'black', label = wyt))
    for x_cnt, x in enumerate(['10%', '20%', '30%', '40%']):
      self.legend_elements.append(Patch(facecolor = 'black', edgecolor = 'black', alpha = float(5-(x_cnt+1))/5.0, label = x))
    self.legend_columns = 2
    self.tickfontsize = 16
