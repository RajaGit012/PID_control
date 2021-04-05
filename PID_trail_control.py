
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation
import numpy as np
import random

###############################################################################

# ONLY CHANGE THESE INPUTS FOR THE CODE TO WORK PROPERLY

# Initialize input values
Number_of_drops=6
trail_inclination=np.pi/6*1 # Keep the angle between 0 and +pi/6 radians
g=10
mass_box=100 # [kg]

# Tune the constants
K_p=300
K_d=300
K_i=10
###############################################################################

Number_of_drops_global=Number_of_drops

# Generate random x-positions for a falling cube
def set_x_ref(trail_inclination):
    rand_h=random.uniform(0,120)
    rand_v=random.uniform(20+120*np.tan(trail_inclination)+6.5,40+120*np.tan(trail_inclination)+6.5)
    return rand_h,rand_v

dt=0.02
t0=0
t_end=5
t=np.arange(t0,t_end+dt,dt)

Force_of_gravity=-mass_box*g

Rail_displacement=np.zeros((Number_of_drops,len(t)))
rail_velocity=np.zeros((Number_of_drops,len(t)))
rail_acceleration=np.zeros((Number_of_drops,len(t)))
pos_x_train=np.zeros((Number_of_drops,len(t)))
pos_y_train=np.zeros((Number_of_drops,len(t)))
e=np.zeros((Number_of_drops,len(t)))
error_diff=np.zeros((Number_of_drops,len(t)))
error_integral=np.zeros((Number_of_drops,len(t)))

cube_position_x=np.zeros((Number_of_drops,len(t)))
cube_position_y=np.zeros((Number_of_drops,len(t)))

Force_oForce_of_gravityravity_tan=Force_of_gravity*np.sin(trail_inclination) # Tangential component of the gravity force
initial_x_position=120
initial_y_position=120*np.tan(trail_inclination)+6.5
initia_box_displacement=(initial_x_position**2+initial_y_position**2)**(0.5)
initial_rail_velocity=0
initial_rail_acceleration=0

initial_x_position_global=initial_x_position # Used for determining the dimensions of the animation window.

Number_of_drops_magn=Number_of_drops
history=np.ones(Number_of_drops)
while(Number_of_drops>0): # Determines how many times cube falls down
    cube_position_x_ref=set_x_ref(trail_inclination)[0] # Cube's initial x position
    cube_position_y_ref=set_x_ref(trail_inclination)[1] # Cube's initial y position
    times=Number_of_drops_magn-Number_of_drops
    cube_position_x[times]=cube_position_x_ref
    cube_position_y[times]=cube_position_y_ref-g/2*t**2
    win=False
    delta=1

    # Implement PID for the train position
    for i in range(1,len(t)):
        # Insert the initial values into the beginning of the predefined arrays.
        if i==1:
            Rail_displacement[times][0]=initia_box_displacement
            pos_x_train[times][0]=initial_x_position
            pos_y_train[times][0]=initial_y_position
            rail_velocity[times][0]=initial_rail_velocity
            rail_acceleration[times][0]=initial_rail_acceleration

        # Compute the horizontal error
        e[times][i-1]=cube_position_x_ref-pos_x_train[times][i-1]

        if i>1:
            error_diff[times][i-1]=(e[times][i-1]-e[times][i-2])/dt
            error_integral[times][i-1]=error_integral[times][i-2]+(e[times][i-2]+e[times][i-1])/2*dt
        if i==len(t)-1:
            e[times][-1]=e[times][-2]
            error_diff[times][-1]=error_diff[times][-2]
            error_integral[times][-1]=error_integral[times][-2]

        F_a=K_p*e[times][i-1]+K_d*error_diff[times][i-1]+K_i*error_integral[times][i-1]
        F_net=F_a+Force_oForce_of_gravityravity_tan
        rail_acceleration[times][i]=F_net/mass_box
        rail_velocity[times][i]=rail_velocity[times][i-1]+(rail_acceleration[times][i-1]+rail_acceleration[times][i])/2*dt
        Rail_displacement[times][i]=Rail_displacement[times][i-1]+(rail_velocity[times][i-1]+rail_velocity[times][i])/2*dt
        pos_x_train[times][i]=Rail_displacement[times][i]*np.cos(trail_inclination)
        pos_y_train[times][i]=Rail_displacement[times][i]*np.sin(trail_inclination)+6.5

        # Try to catch it
        if (pos_x_train[times][i]-5<cube_position_x[times][0]+3 and pos_x_train[times][i]+5>cube_position_x[times][1]-3) or win==True:
            if (pos_y_train[times][i]+3<cube_position_y[times][i]-2 and pos_y_train[times][i]+8>cube_position_y[times][i]+2) or win==True:
                win=True
                if delta==1:
                    change=pos_x_train[times][i]-cube_position_x[times][i]
                    delta=0
                cube_position_x[times][i]=pos_x_train[times][i]-change
                cube_position_y[times][i]=pos_y_train[times][i]+5


    initia_box_displacement=Rail_displacement[times][-1]
    initial_x_position=pos_x_train[times][-1]+rail_velocity[times][-1]*np.cos(trail_inclination)*dt
    initial_y_position=pos_y_train[times][-1]+rail_velocity[times][-1]*np.sin(trail_inclination)*dt
    initial_rail_velocity=rail_velocity[times][-1]
    initial_rail_acceleration=rail_acceleration[times][-1]
    history[times]=delta
    Number_of_drops=Number_of_drops-1


len_t=len(t)-1
frame_rate=int(t_end/dt)*Number_of_drops_global
def update_plot(num):
    #num: 0,1,2,3,4,...,999,1000
    platform.set_data([pos_x_train[int(num/len_t)][num-int(num/len_t)*len_t]-3.1,\
    pos_x_train[int(num/len_t)][num-int(num/len_t)*len_t]+3.1],\
    [pos_y_train[int(num/len_t)][num-int(num/len_t)*len_t],\
    pos_y_train[int(num/len_t)][num-int(num/len_t)*len_t]])

    cube.set_data([cube_position_x[int(num/len_t)][num-int(num/len_t)*len_t]-1,cube_position_x[int(num/len_t)][num-int(num/len_t)*len_t]+1],
    [cube_position_y[int(num/len_t)][num-int(num/len_t)*len_t],cube_position_y[int(num/len_t)][num-int(num/len_t)*len_t]])

    if Number_of_drops_magn*len_t==num+1 and num>0: # All attempts must be successful
        if sum(history)==0:
            success.set_text('CONGRATS! YOU DID IT!')
        else:
            again.set_text('DON’T GIVE UP! YOU CAN DO IT!')

    Rail_displacement_f.set_data(t[0:(num-int(num/len_t)*len_t)],
        Rail_displacement[int(num/len_t)][0:(num-int(num/len_t)*len_t)])

    rail_velocity_f.set_data(t[0:(num-int(num/len_t)*len_t)],
        rail_velocity[int(num/len_t)][0:(num-int(num/len_t)*len_t)])

    rail_acceleration_f.set_data(t[0:(num-int(num/len_t)*len_t)],
        rail_acceleration[int(num/len_t)][0:(num-int(num/len_t)*len_t)])

    e_f.set_data(t[0:(num-int(num/len_t)*len_t)],
        e[int(num/len_t)][0:(num-int(num/len_t)*len_t)])

    error_diff_f.set_data(t[0:(num-int(num/len_t)*len_t)],
        error_diff[int(num/len_t)][0:(num-int(num/len_t)*len_t)])

    error_integral_f.set_data(t[0:(num-int(num/len_t)*len_t)],
        error_integral[int(num/len_t)][0:(num-int(num/len_t)*len_t)])

    return platform,cube,success,again,Rail_displacement_f,rail_velocity_f,rail_acceleration_f,\
        e_f,error_diff_f,error_integral_f


fig=plt.figure(figsize=(16,9),dpi=120,facecolor=(0.8,0.8,0.8))
gs=gridspec.GridSpec(4,3)

# Create game window
ax_main=fig.add_subplot(gs[0:3,0:2],facecolor=(0.9,0.9,0.9))
rail=ax_main.plot([0,initial_x_position_global],[5,initial_x_position_global*np.tan(trail_inclination)+5],'k',linewidth=6)
platform,=ax_main.plot([],[],'b',linewidth=18)
cube,=ax_main.plot([],[],'k',linewidth=14)

plt.xlim(0,initial_x_position_global)
plt.ylim(0,initial_x_position_global)
plt.xticks(np.arange(0,initial_x_position_global+1,10))
plt.yticks(np.arange(0,initial_x_position_global+1,10))
plt.grid(True)

bbox_props_success=dict(boxstyle='square',fc=(0.9,0.9,0.7),ec='g',lw='1')
success=ax_main.text(40,60,'',size='20',color='g',bbox=bbox_props_success)

bbox_props_again=dict(boxstyle='square',fc=(0.9,0.5,0.9),ec='r',lw='1')
again=ax_main.text(30,60,'',size='20',color='r',bbox=bbox_props_again)

copyright=ax_main.text(0,122,'© Mark Misin Engineering',size=12)


# Plot windows
ax1v=fig.add_subplot(gs[0,2],facecolor=(0.5,0.9,0.9))
Rail_displacement_f,=ax1v.plot([],[],'-b',linewidth=2,label='displ. on rails [m]')
plt.xlim(t0,t_end)
plt.ylim(np.min(Rail_displacement)-abs(np.min(Rail_displacement))*0.1,np.max(Rail_displacement)+abs(np.max(Rail_displacement))*0.1)
plt.grid(True)
plt.legend(loc='lower left',fontsize='small')

ax2v=fig.add_subplot(gs[1,2],facecolor=(0.6,0.9,0.7))
rail_velocity_f,=ax2v.plot([],[],'-b',linewidth=2,label='velocity on rails [m/s]')
plt.xlim(t0,t_end)
plt.ylim(np.min(rail_velocity)-abs(np.min(rail_velocity))*0.1,np.max(rail_velocity)+abs(np.max(rail_velocity))*0.1)
plt.grid(True)
plt.legend(loc='lower left',fontsize='small')

ax3v=fig.add_subplot(gs[2,2],facecolor=(0.1,0.6,0.9))
rail_acceleration_f,=ax3v.plot([],[],'-b',linewidth=2,label='accel. on rails [m/s^2] = F_net/m_platf.')
plt.xlim(t0,t_end)
plt.ylim(np.min(rail_acceleration)-abs(np.min(rail_acceleration))*0.1,np.max(rail_acceleration)+abs(np.max(rail_acceleration))*0.1)
plt.grid(True)
plt.legend(loc='lower left',fontsize='small')

ax1h=fig.add_subplot(gs[3,0],facecolor=(0.3,0.9,0.4))
e_f,=ax1h.plot([],[],'-b',linewidth=2,label='horizontal error [m]')
plt.xlim(t0,t_end)
plt.ylim(np.min(e)-abs(np.min(e))*0.1,np.max(e)+abs(np.max(e))*0.1)
plt.grid(True)
plt.legend(loc='lower left',fontsize='small')

ax2h=fig.add_subplot(gs[3,1],facecolor=(0.9,0.1,0.9))
error_diff_f,=ax2h.plot([],[],'-b',linewidth=2,label='change of horiz. error [m/s]')
plt.xlim(t0,t_end)
plt.ylim(np.min(error_diff)-abs(np.min(error_diff))*0.1,np.max(error_diff)+abs(np.max(error_diff))*0.1)
plt.grid(True)
plt.legend(loc='lower left',fontsize='small')

ax3h=fig.add_subplot(gs[3,2],facecolor=(0.7,0.9,0.2))
error_integral_f,=ax3h.plot([],[],'-b',linewidth=2,label='sum of horiz. error [m*s]')
plt.xlim(t0,t_end)
plt.ylim(np.min(error_integral)-abs(np.min(error_integral))*0.1,np.max(error_integral)+abs(np.max(error_integral))*0.1)
plt.grid(True)
plt.legend(loc='lower left',fontsize='small')

pid_ani=animation.FuncAnimation(fig,update_plot,
    frames=frame_rate,interval=20,repeat=False,blit=True)
plt.show()
