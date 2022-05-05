



def map(input_wheel):

    vel_left=512
    vel_rigth=512
    total_vel=1024
    if (velocity>=512):
        if(input_wheel>=0):
            vel_rigth = velocity-total_vel*input_wheel/2
            vel_left = velocity
        if(input_wheel<0):  
            vel_rigth = velocity
            vel_left = velocity+total_vel*input_wheel/2
    if (velocity<512):
        if(input_wheel>=0):
            vel_rigth = velocity
            vel_left = velocity+total_vel*input_wheel/2
        if(input_wheel<0):  
            vel_rigth = velocity-total_vel*input_wheel/2
            vel_left = velocity

    return [int(vel_left),int(vel_rigth)]




input=float(input())
print(map(input)) 