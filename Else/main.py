#Använd funktion i image_processing_module som checkar att kryssets position är detekterat.
#Kopplas till user_interface_module
# (FUNKTIONEN BEHÖVER GÖRAS)

#Koppla startknapp i user_interface_module till start_recording() i camera_control_module. 

#Koppla stoppknapp i user_interface_module till stop_recording() i camera_control_module.

#I camera_control_module använd funktion som checkar att mobilerna gjorde en video.
#Ska kopplas till user_interface_module så man ser att mobilerna filmade.
# (FUNKTIONEN BEHÖVER BYGGAS)

#I camera_control_module använd funktion som ger filepath till den nyss tagna videon för de två mobilerna.
# (FUNKTIONEN BEHÖVER BYGGAS)

#Gör ett objekt för de två videorna till image_processing_module

#I image_processing_module använd funktionen detect_dodgeball()

#I image_processing_module använd funktionen detect_target()

#Gör ett objekt för de två positionerna givna från detect_dodgeball()

#I data_analysis_module använd funktionen calculate_velocity() 

#I data_analysis_module använd funktionen calculate_accuracy(target) 
# där target fås med funktionen detect_target() från image_processing_module)

#I data_storage_module använd funktionen save_measurement() om mätningen var lyckad.

#Använd funktionen retrieve_measurements() ihop med user_interface_module 
#för att presentera resultatet i appen
