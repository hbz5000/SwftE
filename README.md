# Storing Water for the Environment (SwftE)
This repository contains all code and data to evaluate tradeoffs associated with Storing Water for the Environment (SwftE) in a hypothetical river basin with surface water storage, modeled after the Sacramento River Basin and Shasta Reservoir.  SwftE evaluates how dedicating a portion of surface water storage and/or inflows to environmental purposes impacts ecosystem temperature/flow objectives and what, if any, impact this has on deliveries to existing water uses, including in-basin M&I/Ag consumption, 'system' water needs (e.g., salinity control in a delta), wetland wildlife refuges, and exports to users outside of the basin.


## Installation and setup
1. Clone this repository to your local machine.
2. Ensure that the following python packages are installed via pip or conda:
    a. datetime
	b. pandas
	c. numpy
	d. matplotlib
	e. seaborn
	f. calendar
3. Create the folder 'swfte_figures' inside the main SwftE directory
4. From the base SwftE directory, run model with ``python swfte_main.py
5. The SwftE model will run, printing the names of figures as it prints them
6. Figures in the swfte_figures folder re-create the figures in the Technical Appendix to the report 'Storing Water for the Environment', which can be found: (permanent link to report)