# Contam Weather Study Code - AJE
This repository contains the code and data to reproduce the research contained in the manuscript "Assessing the effects of transient weather conditions on airborne transmission risk in naturally ventilated hospitals."; Alexander J. Edwards, Marco-Felipe King,  Martin Lopez-Garcia, Daniel Peckham, Catherine J. Noakes.

# Software
This code is written using Python in Spyder 4.1.4. Users will also require CONTAM 3.4.0.3 to reproduce the airflow simulations.

# Description
1. To reproduce the concentration of pathogen solution and predicted exposure solution for 'natural ventilation only':
Use script 'NatVentOnly/Contam_12zone_AJE.py' for the full 6-month solution of the quanta concentration and predicted exposures. Use script 'NatVentOnly/Exposure_weekly_outbreaks_AJE.py' for the weekly exposures study, providing the results to be used for the predicted exposure analysis. Note the default infector location is Zone 5. To change this, this should be edited in the main script 'NatVentOnly/Contam_12zone_AJE.py' or 'NatVentOnly/Exposure_weekly_outbreaks_AJE.py', for the concentration or exposure study, respectively. Set I_zonal[k]=1 for Infector in Zone k.
These scripts uses the following scripts to run:
* 'NatVentOnly/ventflows_AJE.py' to set-up the ventilation matrix and inverse ventialtion matrix.
* 'NatVentOnly/Extract_AJE' to set up the natural ventialtion rates which are exported from CONTAM.
* 'IZFlows_AJE.py' to set up the inter-zonal flow and natural ventilation values imported from CONTAM.
* 'SE_Conc_eqns_AJE.py' contains the odes for the concentration transport system, and the suscpetible-exposed model which are solved in the code.
* 'Contam_sim/IZFlows.csv' contains the inter-flow rates which should be set as the defined filepath in each of the above scripts to extract the results from the contam simulation.



2. To reproduce the concentration of pathogen solution and predicted exposure solution for 2 cases of 'Natural ventialtion and Mechanical' and 'mechanical ventilation only':
Use script 'MechVent/Contam_12zone_MV_AJE.py' for the full 6-month solution of the quanta concentration and predicted exposures. Use script 'MechVent/Exposure_weekly_MV_AJE.py' for the weekly exposures study, providing the results to be used for the predicted exposure analysis.
These scripts uses the following scripts to run:
* 'MechVent/ventflows_MV_AJE.py' to set-up the ventilation matrix and inverse ventialtion matrix.
* 'MechVent/Extract_MV_AJE' to set up the natural ventialtion rates (where applicale) and the mechanical ventialtion rates which are exported from CONTAM.
* 'IZFlows_AJE.py' to set up the inter-zonal flow values imported from CONTAM.
* 'SE_Conc_eqns_AJE.py' contains the odes for the concentration transport system, and the suscpetible-exposed model which are solved in the code.
* 'Contam_sim/IZFlow_MV_windclsd3ACH.csv' contains the inter-flow rates and natural ventilation rates which should be set as the defined filepath for airflow solutions when conidering 'Mechanical Ventilation Only' case.
* 'Contam_sim/IZFlow_MV_windop3ACH.csv' contains the inter-flow rates and natural ventilation rates which should be set as the defined filepath for airflow solutions when conidering 'Natural Ventialtion and Mechanical Ventilation' case.
* 'Contam_sim/MechVentFlows3ACH.csv' contains the Mechancial ventialtion flow rates which should be set as the defined filepath for mechanical ventialtion solutions when conidering 'Natural Ventialtion and Mechanical Ventilation' case and the 'Mechanical Ventilation Only' case.


3. For the comparison of simulated CO2 values with measured CO2 data use the following:
* 'measured_co2_data.csv' containes the measured CO2 data from the EPSRC HECOIRA Project.
* 'Contam_sim/CO2_data_OctOnly.csv' contains the siulasted CO2 data from the CONTAM simulation.


4. For the CO2 Analysis: 'Contam_sim/Co2_data.csv' contains all of the simulated CO2 data for each zone.


5. The weather file used throughout can be found in 'GBR_ENG_Leeds.Gen.wth'.
