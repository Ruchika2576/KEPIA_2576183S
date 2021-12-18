import requests
from utils import constants as const
import json
import streamlit as st
import concurrent.futures
import time
from time import sleep

# This module deals with all the API calls made to KAL

def get_response_from_KAL(single_instance, single_operation,single_altruistic_chain_length):
    #Extracting the json dictionary into KEP instances and recipients
    payload = None

    kep_single_instance = single_instance[const.data]
    recipients = single_instance[const.recipients]

    #Creating request params to call the Kidney Exchange allocator
    kep_single_instances_dict = {const.data: kep_single_instance}

    kep_single_instance_obj  = {
    const.operation: single_operation,
    const.altruistic_chain_length: int(single_altruistic_chain_length),
    const.data: json.dumps(kep_single_instances_dict)
    }

    try:
        response = requests.post(const.kidney_exchange_allocator_url, data = kep_single_instance_obj)
        if response.status_code == 200:
            payload = response.json()
        else:
            st.error(f"Request returned: {response.status_code} : '{response.reason}'")
            raise RuntimeError(const.error4)
    except Exception as exc:
        st.error(const.error5 )
        st.error(exc)

    return payload

# Individual requests fucntion
def get_data_from_NHS_one_request(session,kep_instance_obj):

    response = session.send(requests.Request('POST',const.kidney_exchange_allocator_url, data = kep_instance_obj ).prepare())
    payload =  response.json()

    return payload
# The fuction spawns the thread and calls get_data_from_NHS_one_request on each request
def create_multithread_for_NHS_request(multi_uploaded_zip_instance,operation,altruistic_chain_length ):

    payload_list =[]
    instance_obj_list = []
    future_list = []
    for instance in multi_uploaded_zip_instance:


        kep_instance = instance[const.data]

        #Creating request params to call the Kidney Exchange allocator
        kep_instances_dict = {const.data: kep_instance}

        kep_instance_obj  = {
        'operation': operation,
        'altruistic_chain_length': int(altruistic_chain_length),
        const.data: json.dumps(kep_instances_dict)
        }
        instance_obj_list.append(kep_instance_obj)

#create an thread and a  session, to handle all the requests
    with concurrent.futures.ThreadPoolExecutor(max_workers = 200) as executor:
        with requests.Session() as session:

            for kep_instance_obj in instance_obj_list:

                futures = executor.submit(get_data_from_NHS_one_request,session = session ,kep_instance_obj =kep_instance_obj)
                future_list.append(futures)

            for future in concurrent.futures.as_completed(future_list):
                #st.write('length ' + str(len(future_list)))
                try:
                    payload_list.append(future.result())
                except requests.ConnectTimeout:
                    print("ConnectTimeout.")

    return payload_list

# This thread divides the number of inputs into batches of 50
@st.cache(suppress_st_warning = True)
def get_data_NHS_Optimal(multi_uploaded_zip_instance,operation, altruistic_chain_length):
    length = len(multi_uploaded_zip_instance)
    rem = length % 50
    loops = (length-rem)//50
    payload_list = None
    final_payload_list = []

    k = 0
    a = 0

    if len(multi_uploaded_zip_instance) > 50:
        for i in range(0,loops):
            # st.write('---------beginning loop :' + str(i) +'----------')
            a = k+49
            sub_instances = []
            for j in range(k,a+1):
                sub_instances.append(multi_uploaded_zip_instance[j])
            st.write('length of sub list:', str(len(sub_instances)))
            start = time.time()
            st.write('sleeping for 60 seconds')
            sleep(400)
            payload_list = create_multithread_for_NHS_request(sub_instances,operation,altruistic_chain_length )
            final_payload_list.extend(payload_list)
            end = time.time()
            st.write('time taken execute this loop' + str(i) + ':' + str((end-start)/60) + 'minutes')
            k = a+1


        if rem !=0:
            # st.write('---------remaining list----------')
            sub_instances = []
            for i in range(a, length):
                sub_instances.append(multi_uploaded_zip_instance[i])
            st.write('length of sub list:', str(len(sub_instances)))
            payload_list = create_multithread_for_NHS_request(sub_instances,operation,altruistic_chain_length )
            final_payload_list.extend(payload_list)

        return final_payload_list

    else:
        # st.write('---------List is less than 50----------')
        payload_list = create_multithread_for_NHS_request(multi_uploaded_zip_instance,operation,altruistic_chain_length )
        return payload_list

# Commented code for trying different methods for calling nhs api
# #direct call
# def get_all_response_from_KAL(multi_uploaded_zip_instance,operation, altruistic_chain_length):
#     payload_list = []
#     a = []
#
#     for instance in multi_uploaded_zip_instance:
#         payload = get_response_from_KAL(instance, operation,altruistic_chain_length)
#         payload_list.append(payload)
#     st.write('payload list' + str(len(payload_list)))
#
#
#
#     return payload_list
#
# def get_response_from_KAL(instance, operation,altruistic_chain_length):
#     #Extracting the json dictionary into KEP instances and recipients
#
#     kep_instance = instance[const.data]
#     recipients = instance[const.recipients]
#
#     #Creating request params to call the Kidney Exchange allocator
#     kep_instances_dict = {const.data: kep_instance}
#
#     kep_instance_obj  = {
#     'operation': operation,
#     'altruistic_chain_length': int(altruistic_chain_length),
#     const.data: json.dumps(kep_instances_dict)
#     }
#
#     try:
#         response = requests.post(kidney_exchange_allocator_url, data = kep_instance_obj)
#     except Exception as exc:
#         st.error('Error ocurred while fetching data from https://kidney-nhs.optimalmatching.com/' )
#         st.error(exc)
#
#     if response.status_code == 200:
#         payload = response.json()
#     else:
#         st.error(f"Request returned: {response.status_code} : '{response.reason}'")
#         raise RuntimeError('Error in Response from https://kidney-nhs.optimalmatching.com/')
#
#
#     return payload





    #payload_list = get4(multi_uploaded_zip_instance,operation, altruistic_chain_length)


# @gen.coroutine
# def get6(multi_uploaded_zip_instance,operation,altruistic_chain_length ):
#     #create an aiohttp session, to handle all the requests
#     payload_list =[]
#     instance_obj_list = []
#     future_list = []
#     http_client = httpclient.AsyncHTTPClient()
#
#     for instance in multi_uploaded_zip_instance:
#
#         #this function will perform the actual request
#         kep_instance = instance[const.data]
#
#         #Creating request params to call the Kidney Exchange allocator
#         kep_instances_dict = {const.data: kep_instance}
#
#         kep_instance_obj  = {
#         'operation': operation,
#         'altruistic_chain_length': int(altruistic_chain_length),
#         const.data: json.dumps(kep_instances_dict)
#         }
#         instance_obj_list.append(kep_instance_obj)
#
#         request = httpclient.HTTPRequest(kidney_exchange_allocator_url,body = kep_instance_obj, method = 'POST' )
#         response = yield http_client.fetch(request)
#         payload_list.append(response)
#
#     return payload_list
# #asynchronous call
# async def get1(multi_uploaded_zip_instance,operation,altruistic_chain_length ):
#     #create an aiohttp session, to handle all the requests
#     payload_list =[]
#     i = 0
#     async with aiohttp.ClientSession() as session:
#         #create task: each individual requests
#         tasks = []
#         for instance in multi_uploaded_zip_instance:
#
#             #this function will perform the actual request
#             kep_instance = instance[const.data]
#
#             #Creating request params to call the Kidney Exchange allocator
#             kep_instances_dict = {const.data: kep_instance}
#
#             kep_instance_obj  = {
#             'operation': operation,
#             'altruistic_chain_length': int(altruistic_chain_length),
#             const.data: json.dumps(kep_instances_dict)
#             }
#
#             # task = asyncio.ensure_future(get2(session, kep_instance_obj))
#             task = get2(session, kep_instance_obj)
#             tasks.append(task)
#
#         payload_list = await asyncio.gather(*tasks)
#         return payload_list
#
# async def get2(session,kep_instance_obj):
#
#     async with session.post(kidney_exchange_allocator_url, data = kep_instance_obj ) as response:
#
#         payload = await response.json()
#
#         return payload

#Reading Files from firebase
# def get_files_from_firebase():
#     storage = get_firebase_connection()
#     all_files = storage.list_files()
#     instance_list = []
#     for file in all_files:
#         url = storage.child(file.name).get_url(None)
#         f = urllib.request.urlopen(url).read()
#         instance = json.loads(f)
#         instance_list.append(instance)
