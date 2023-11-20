# Contam Weather Study Code - AJE
This repository contains the code and data to reproduce the research contained in the manuscript "Assessing the effects of transient weather conditions on airborne transmission risk in naturally ventilated hospitals."; Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.

# Software
This code is written using Python in Spyder 4.1.4. Users will also require CONTAM 3.4.0.3 to reproduce the airflow simulations.

# Description
1. To reproduce the concentration of pathogen solution and predicted exposure solution for 'natural ventilation only':
Use script 'NatVentOnly/Contam_12zone_AJE.py' for the full 6-month solution of the quanta concentration and predicted exposures. Use script 'NatVentOnly/Exposure_weekly_outbreaks_AJE.py' for the weekly exposures study, providing the results to be used for the predicted exposure analysis. Note the default infector location is Zone 5. To change this, this should be edited in the main script 'NatVentOnly/Contam_12zone_AJE.py' or 'NatVentOnly/Exposure_weekly_outbreaks_AJE.py', for the concentration or exposure study, respectively. Set I_zonal[k]=1 for Infector in Zone k, and at the end of the script, in the plotting section only, adjust K_zonal[k] to be the new total number of susceptible in zone k.
These scripts use the following to run:
* 'NatVentOnly/ventflows_AJE.py' to set-up the ventilation matrix and inverse ventialtion matrix.
* 'NatVentOnly/Extract_AJE' to set up the natural ventialtion rates which are exported from CONTAM.
* 'IZFlows_AJE.py' to set up the inter-zonal flow and natural ventilation values imported from CONTAM.
* 'read_csv_AJE' is used within 'NatVentOnly/Extract_AJE' and 'IZFlows_AJE.py' to read the excel .csv file with the exported CONTAM results.
* 'SE_Conc_eqns_AJE.py' contains the odes for the concentration transport system, and the suscpetible-exposed model which are solved in the code.
* 'geom_code_AJE.py' contains the code to plot the heat map for the output results. This script requires a file path to the image of the required geometry, in this case a 12-zone hospital ward found in '12zone_geom.png'. Please note that the star to indicate the infectors location is added manually after producing the heat map.
* 'Contam_sim/IZFlows.csv' contains the inter-flow rates and natural ventilation rates which should be set as the defined filepath in each of the above scripts to extract the results from the contam simulation when considering the Natural Ventilation Doors Closed case.
* 'Contam_sim/IZFlows_opbay.csv' contains the inter-flow rates and natural ventilation rates which should be set as the defined filepath in each of the above scripts to extract the results from the contam simulation when considering the Natural Ventilation Doorss Open case.


2. To reproduce the concentration of pathogen solution and predicted exposure solution for 2 cases of 'Natural ventialtion and Mechanical Ventialtion' for different ventialtion rates, 3 ACH and 6 ACH:
Use script 'MechVent/Contam_12zone_MV_AJE.py' for the full 6-month solution of the quanta concentration and predicted exposures. Use script 'MechVent/Exposure_weekly_MV_AJE.py' for the weekly exposures study, providing the results to be used for the predicted exposure analysis. Note: the user should uncomment and define the appropriate file path at the beginning of the script depending on which scenario to run (windows closed or windows open). The corresponding file path should be defined under the variable 'filepath'. 
These scripts use the following to run:
* 'MechVent/ventflows_MV_AJE.py' to set-up the ventilation matrix and inverse ventialtion matrix.
* 'MechVent/Extract_MV_AJE' to set up the natural ventialtion rates and the mechanical ventialtion rates which are exported from CONTAM.
* 'IZFlows_AJE.py' to set up the inter-zonal flow values imported from CONTAM.
* 'read_csv_AJE' is used within 'NatVentOnly/Extract_AJE' and 'IZFlows_AJE.py' to read the excel .csv file with the exported CONTAM results.
* 'SE_Conc_eqns_AJE.py' contains the odes for the concentration transport system, and the suscpetible-exposed model which are solved in the code.
* 'Contam_sim/IZFlow_MV_windop3ACH.csv' contains the inter-flow rates and natural ventilation rates which should be set as the defined filepath for airflow solutions when conidering 'Natural Ventialtion and 3 ACH Mechanical Ventilation 3ACH' case.
* 'Contam_sim/MechVentFlows3ACH.csv' contains the Mechancial ventialtion flow rates which should be set as the defined filepath for mechanical ventialtion solutions when conidering 'Natural Ventialtion and 3 ACH Mechanical Ventilation' case.
* 'Contam_sim/IZFlow_MV_windop6ACH.csv' contains the inter-flow rates and natural ventilation rates which should be set as the defined filepath for airflow solutions when conidering 'Natural Ventialtion and 6 ACH Mechanical Ventilation 3ACH' case.
* 'Contam_sim/MechVentFlows6ACH.csv' contains the Mechancial ventialtion flow rates which should be set as the defined filepath for mechanical ventialtion solutions when conidering 'Natural Ventialtion and 6 ACH Mechanical Ventilation' case.
* 'geom_code_AJE.py' contains the code to plot the heat map for the output results. This script requires a file path to the image of the required geometry, in this case a 12-zone hospital ward found in '12zone_geom.png'. Please note that the star to indicate the infectors location is added manually after producing the heat map.


3. For the comparison of simulated CO2 values with measured CO2 data use the script 'CO2_analysis/CO2_validation_AJE.py' which uses the following:
* 'CO2_analysis/measured_co2_data.csv' containes the measured CO2 data from the EPSRC HECOIRA Project.
* 'CO2_analysis/CO2_data_OctOnly_Allclsd.csv' contains the simulated CO2 data from the CONTAM simulation for the scenario with all of the doors closed.
* 'CO2_analysis/CO2_data_OctOnly_Halfclsd.csv' contains the simulated CO2 data from the CONTAM simulation for the scenario with half of the doors closed (only patient bays).
* 'read_csv_gen_AJE' is used to read the excel .csv file with the exported CONTAM results.


4. For the general CO2 Analysis plot using the simulated CO2 data from CONTAM, one should run the script 'CO2_analysis/CO2_plot_AJE.py', which uses the following:
* 'CO2_analysis/Co2_data.csv' contains all of the simulated CO2 data for each zone which is used in the script and the location of this file should be set as the filepath in the script.
* 'CO2_analysis/read_csv_co2_AJE.py' is used to read the simulated CO2 data from the CONTAM simulation.


5. The weather file used throughout can be found in 'GBR_ENG_Leeds.Gen.wth'.

6. For the plotting of the natural ventialtion rates achieved use the script labelled 'VentRates/nat_vent_AJE.py'. This script uses the following scripts:
* 'VentRates/geom_code_natvent_AJE.py' this contains the heat map code for the natural ventialtion case.
* 'NatVentOnly/ventflows_AJE.py' to set-up the ventilation matrix and inverse ventialtion matrix.
* 'NatVentOnly/Extract_AJE' to set up the natural ventialtion rates which are exported from CONTAM.
* 'read_csv_AJE' is used within 'NatVentOnly/Extract_AJE' and 'IZFlows_AJE.py' to read the excel .csv file with the exported CONTAM results.
* 'Contam_sim/IZFlows.csv' contains the inter-flow rates and natural ventilation rates which should be set as the defined filepath in each of the above scripts to extract the results from the contam simulation.
* 'geom_code_natvent_AJE.py' contains the code to plot the heat map for the output results. This script requires a file path to the image of the required geometry, in this case a 12-zone hospital ward found in '12zone_geom.png'. Please note that the star to indicate the infectors location is added manually after producing the heat map.



Note: All of the above scripts and sub-folders need to be added to the working path in path manager. 
