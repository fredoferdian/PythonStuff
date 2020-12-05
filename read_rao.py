# preamble
import numpy as np
import os
#import matplotlib
import matplotlib.pyplot as plt
# color package
from matplotlib import colors as mcolors
colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
# picture font options
import matplotlib.ticker as ticker
from matplotlib.ticker import FormatStrFormatter
#majorLocator = MultipleLocator(20)
#majorFormatter = FormatStrFormatter('%d')
#minorLocator = MultipleLocator(5)
from matplotlib import rcParams
rcParams['font.sans-serif'] = ['Arial'] #fonttype
xdim = 6.3  # inches (16 cm)
ydim = 4.33 # inches (10 cm)
rcParams['figure.figsize'] = xdim, ydim #set size of figure
#font sizes for plot
SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 14
#
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
#
#color vector
color_vec = ['blue',
             'firebrick',
             'darkgreen',
             'dodgerblue',
             'darkorange',
             'limegreen' ]
#marker vector
marker_vec = ['s',
              '^',
              'p',
              'D',
              'v',
              '.'
              ]
# set auto axis
auto_xaxis = 0
auto_yaxis1 = 0
auto_yaxis2 = 0
# values for x and y limits
lim_xaxis = (0,26) # periods
lim_yaxis1 = (0,12) # translation
lim_yaxis2 = (0,39) # rotation
#
auto_phase_xaxis = 0
auto_phase_yaxis1 = 0
auto_phase_yaxis2 = 0
#values for x and y limits
lim_phase_xaxis = (0, 0)
lim_phase_yaxis1 = (0, 0)
lim_phase_yaxis2 = (0, 0)
# ENVIRONMENT
#
plot_data = 1
#
Hs = [1.00, 1.25, 1.50, 2.00]
Tp = 3
v_ah = [0.00] #forward speed
#Heading = [0, 90, 180, 270]
Heading = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
env = 'e'
env_num = 0
count_env = -1
env_list = []

environment = dict() # store all numbered env in environment dictionary

for hs in range(len(Hs)): # loop wave height
    Tp1 = np.sqrt(13*Hs[hs])
    Tp3 = np.sqrt(30*Hs[hs])
    Tp2 = np.mean((Tp1,Tp3)) 
    TP = np.array([Tp1, Tp2, Tp3])
    for head in range(len(Heading)):    #loop heading
        for tp in range(3):             #loop wave period
            env_num += 1
            env_list.append(env+(str(env_num).zfill(3)))
            for vah in range(len(v_ah)):
                count_env += 1
                env_list[count_env] = (env_list[count_env]+'_'+str(v_ah[vah])[0:-2])
                temp_env = np.array([Heading[head],Hs[hs],TP[tp],v_ah[vah]])
                env_entry = {env_list[count_env]:temp_env}
                environment.update(env_entry)
                env_list.append(env+(str(env_num).zfill(3)))
#
#
#
#read directories from folder
dir_list = []
# path of MOSES .ans folder
path = 'G:\\data (hh)\\marine\\M1007 PETROFOR Pickerill Decommission\\CTR 40 Marine\\CAL\\for REP\\002 - Motion Analysis\\m1007.ans\\'
# save path
saveroot = 'G:\\data (hh)\\marine\\M1007 PETROFOR Pickerill Decommission\\IWF\\JWE\\Motion Report\\'

#
for directories in os.listdir(path):
    if directories != 'lsw' and  directories != 'lc_0':
#        print('no lsw')
#    elif  directories != 'lc_0':
        if os.path.isdir(path+'\\'+directories):
            dir_list.append(directories)    # store all folder names except lsw
#
#
# loop directories ins .ans folder
filenames = []
mota_files = []
for dir_count in dir_list:
    data_path = path+'\\'+dir_count+'\\fdom\\raos'
    for file_count in os.listdir(data_path):
        if file_count.endswith('.txt'):
            filenames.append(data_path+'\\'+file_count) # save path of all txt files in RAO folder
    data_path = path+'\\'+dir_count+'\\fdom\\motacc'
    for mota_count in os.listdir(data_path):
        mota_files.append(data_path+'\\'+mota_count) # save path of all html tables (motacc data)
#
#
#
count_plot = 0
env_count = 0
new_folder = False
#
if plot_data == 1:
    for plot in filenames:
        filename = filenames[count_plot]
        # 
        #read table
        data = (np.genfromtxt((filename),
                        dtype = None,                           
                        skip_header = 26,
                        usecols = (0,1,2,3,4,5,6,7,8,9,10,11,12,13),
                        names=('freq','T','surge','p_surge','sway','p_sway','heave','p_heave','roll','p_roll','pitch','p_pitch','yaw','p_yaw'))
                        )
        #read info from header
        # if filenames is halfway through environments need to start at 0 again
        # first half contains data for grillage height 3 m
        # second half contains fata for girllage height 18.5 m
#        if count_plot == (len(filenames)/2):
#            env_count = 0
#            new_folder = True
        
        row_counter = 0
        with open(filename, 'r') as file:           #open file and allow to read / var name file
            for line in file:
                row_counter += 1                    #count rows
                if not line.split(): continue
                linedata = line.split()             #use linedata to store strings from line split
                
                if row_counter < 7:                 #do nothing if row_counter is < 7 
                    continue
                elif row_counter > 9:               #break loop if row_counter > 9
                    break
                
                info_data = linedata
                if info_data[1] == 'Draft':         # use vars to store data
                    draft = info_data[3]
                    trim = info_data[8]
                    gmt = info_data[12]
                if info_data[1] == 'Roll':
                   gyr_roll = info_data[5]
                   gyr_pitch = info_data[11]
                   gyr_yaw =    info_data[17]
                if info_data[1] == 'Heading':
                    heading = info_data[3]
                    v_vessel = info_data[8]
                    env_name = info_data[13]
        del info_data
        del row_counter
        del linedata
        #
        # additional data
        env = env_list[env_count]
        print('env is '+env)
        H = environment[env][1]
        H = format(H,'.2f')
        T = environment[env][2]
        T = format(T, '.2f')
        #
        # create plots
        label_vec = ['Surge','Sway','Heave','Roll','Pitch','Yaw']
        x_data = np.flip(data['T'],0)
        y_data = (data['surge'],data['sway'],data['heave'],data['roll'],data['pitch'],data['yaw'])
        #
        fig,ax1 = plt.subplots()
        ## translation
        #surge
        ax1.plot(x_data, np.flip(data['surge'],0),  #flip y to plot an increasing vector
                 '.-',
                 linewidth = 0.5,
                 label=label_vec[0],
                 color = colors[color_vec[0]],
                 marker = marker_vec[0],
                 markersize = 2
                 )
        #sway
        ax1.plot(x_data, np.flip(data['sway'],0),  #flip y to plot an increasing vector
             '.-',
             linewidth = 0.5,
             label=label_vec[1],
             color = colors[color_vec[1]],
             marker = marker_vec[1],
             markersize = 2
             )
        #heave
        ax1.plot(x_data, np.flip(data['heave'],0),  #flip y to plot an increasing vector
                 '.-',
                 linewidth = 0.5,
                 label=label_vec[2],
                 color = colors[color_vec[2]],
                 marker = marker_vec[2],
                 markersize = 3
                 )
        ax1.tick_params(axis = 'y')
        # set ticklabel xaxis
        ax1.xaxis.set_major_locator(ticker.MultipleLocator(2.0))    # tick for every 2.0 value
        if auto_xaxis == 0:
            ax1.set_xlim(lim_xaxis)
        if auto_yaxis1 == 0:
            ax1.set_ylim(lim_yaxis1)
        # set ticklabel yaxis
        ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.5))    # tick for every 0.5 value
        ## rotation
        ax2 = ax1.twinx()
        #roll   
        ax2.plot(x_data, np.flip(data['roll'],0),  #flip y to plot an increasing vector
                 '.-',
                 linewidth = 0.5,
                 label=label_vec[3],
                 color = colors[color_vec[3]],
                 marker = marker_vec[3],
                 markersize = 2
                 )
        #pitch   
        ax2.plot(x_data, np.flip(data['pitch'],0),  #flip y to plot an increasing vector
                 '.-',
                 linewidth = 0.5,
                 label=label_vec[4],
                 color = colors[color_vec[4]],
                 marker = marker_vec[4],
                 markersize = 2
                 )
        #yaw  
        ax2.plot(x_data, np.flip(data['yaw'],0),  #flip y to plot an increasing vector
                 '.-',
                 linewidth = 0.5,
                 label=label_vec[5],
                 color = colors[color_vec[5]],
                 marker = marker_vec[5],
                 markersize = 3
                 )
        ax2.tick_params(axis = 'y')
        if auto_xaxis == 0:
            ax2.set_xlim(lim_xaxis)
        if auto_yaxis2 == 0:
            ax2.set_ylim(lim_yaxis2)
        
        ax1.legend(loc='upper center', bbox_to_anchor=(0.27, -0.15), ncol = 3,frameon = False)
        ax2.legend(loc='upper center', bbox_to_anchor=(0.73, -0.15), ncol = 3,frameon = False)
        ax1.set_xlabel('Encounter Wave Period in s')
        ax1.set_ylabel('Translation in m/(m amplitude wave)')
        ax1.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    
        ax2.set_ylabel('Rotation in deg/(m amplitude wave)')
        ax2.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        plt.title("Motion Response Amplitude Operator \n")
        plt.suptitle(f"Heading = {heading} deg, Forward Speed = {v_vessel} kn, Hs = {H} m, Tp = {T} s",fontsize = 10,y =0.92)
        #
        #save figure
        fig.tight_layout() 
        if new_folder == True:
            # path for saving plots
            savefolder = 'motion\\'
            fig.savefig((saveroot+savefolder+env+'_hs'+H+'_heading'+heading[:heading.index(".")]+'_rao.png'),dpi=300, bbox_inches="tight")
        else:
            savefolder = 'motion\\'
            fig.savefig((saveroot+savefolder+env+'_hs'+H+'_heading'+heading[:heading.index(".")]+'_rao.png'),dpi=300, bbox_inches="tight") # savepath, dpi, dont cut off title when saving
        plt.close('all')
        #
        #
        #
        print('files (RAOs) completed:',count_plot,'/',len(filenames))
        # and 1 for count_plot
        count_plot += 1
        env_count += 1
        if count_plot == len(filenames):
            print('files (RAOs) completed:',count_plot,'/',len(filenames))
            print('Motion RAOs completed')