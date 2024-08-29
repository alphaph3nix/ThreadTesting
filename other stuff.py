###############################################################example of handling multiple ports
# ae_scp_c_store = AE(ae_title="scp_c_store")
# ae_scp_c_store.supported_contexts = AllStoragePresentationContexts
# # ae_scp_c_store._require_called_aet=True
# ae_scp_c_store.start_server(('192.168.1.34', 11113), block=False, evt_handlers=[handlers[0]])
# logging.info("Starting scp_c_store on port 11113")

# ae_scp_c_echo = AE(ae_title="scp_c_echo")
# ae_scp_c_echo.supported_contexts = VerificationPresentationContexts
# # ae_scp_c_echo._require_called_aet=True
# ae_scp_c_echo.start_server(('localhost', 11114), block=False, evt_handlers=[handlers[1]])
# logging.info("Starting scp_c_echo on port 11114")

# input("type to exist\n")


######################################################################################example of send n action in scu
 # action_ds = Dataset()
                # action_ds.ReferencedSOPClassUID = dataset.SOPClassUID
                # action_ds.ReferencedSOPInstanceUID = dataset.SOPInstanceUID

                # # status = assoc.send_n_action(class_uid=dataset.SOPClassUID,instance_uid=dataset.SOPInstanceUID,msg_id=1,action_type=1)
                # status = assoc.send_n_action(action_ds,1,dataset.SOPClassUID,dataset.SOPInstanceUID,1)

                # if status == 0x0000:
                #     print("Storage Commitment demandé avec succès.")
                # else:
                #     print(f"Échec de la demande de Storage Commitment: {status}")