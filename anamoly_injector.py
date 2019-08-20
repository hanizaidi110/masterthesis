# stress CPU - answer restart service

#Start a stress CPU anomaly. Set the number of cores to 2 and the stress level to 80%:
#curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"parameter":"--cpu=2 --cpu-load=80"}' 0.0.0.0:7999/api/anomalies/stress_cpu/

#Stop the stress_cpu anomaly:
#curl -X DELETE 0.0.0.0:7999/api/anomalies/stress_cpu/

#Get a list of all running anomalies:
#curl -X GET 0.0.0.0:7999/api/anomalies/


#####-----------------------------------------------------####
# stress through client - answer scale up

# curl -X POST -T http://0.0.0.0:7777/api/streams -H {"num"=60}


#####-----------------------------------------------------####
# memory cache delete ~


#####-------------Recording Impact before and after---------------####




