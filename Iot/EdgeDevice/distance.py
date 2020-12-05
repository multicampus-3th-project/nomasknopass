from gpiozero import DistanceSensor

def human_waytogo():
    global hmn_state
    prnt_hmn_dist = sensor.distance
    while True:
        time.sleep(0.2)
        past_hmn_dist = prnt_hmn_dist
        prnt_hmn_dist = sensor.distance
        if (past_hmn_dist>PASS_ZONE and prnt_hmn_dist < PASS_ZONE and prnt_hmn_dist > 0 ):
            print("human passed")
            hmn_state = 1
        elif (past_hmn_dist<CHECK_ZONE and prnt_hmn_dist > CHECK_ZONE):
            print("human returned")
            hmn_state = 2
        elif (past_hmn_dist>CHECK_ZONE and prnt_hmn_dist < CHECK_ZONE and prnt_hmn_dist > PASS_ZONE ):
            print("human approached")
            hmn_state = 3
        else :
            continue
        print("distance {0:.4f}, and state {0:.d}".format(sensor.distance, hmn_state))