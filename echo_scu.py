from pynetdicom import AE, evt, VerificationPresentationContexts,debug_logger
from pynetdicom import build_context

def send_c_echo(aet,addr,port,aec):
    debug_logger()
    ae = AE(ae_title=aet)
    cx = build_context('1.2.840.10008.1.1', ['1.2.840.10008.1.2'])        #Abstract Syntax: 1.2.840.10008.1.1(Verification SOP Class) /// Transfer Syntax: 1.2.840.10008.1.2 (Implicit VR Little Endian) 
    # ae.requested_contexts = VerificationPresentationContexts
    ae.requested_contexts= [cx]

    try:
        # Establish Association
        assoc = ae.associate(addr=addr,port=port,ae_title=aec)
        status=None

        if assoc.is_established:
            print(f'sending c echo to {addr}:{port} with AET={aec} ')
            status = assoc.send_c_echo()
            # Release the association
            assoc.release()

    except Exception as e:
        print(e)

    print(status)
  



if __name__ == "__main__":
    # send_c_echo('127.0.0.1',104,'PACS' )
    send_c_echo("CALLING_AE",'127.0.0.1',104,'CALLED_AE' )
    # send_c_echo('127.0.0.1',105,'PACS' )
    # send_c_echo('127.0.0.1',106,'PACS' )
    
    
