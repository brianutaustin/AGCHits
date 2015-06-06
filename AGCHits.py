#!/usr/bin/env python
import argparse
import numpy as np
import matplotlib.pyplot as plt
import root_numpy as rnp
from scipy import signal as signal

def parse_run(file_path):
    token_list = file_path.split("_")
    run = token_list[2]
    return run

def get_event(v1751_array, board, run, spill, event):

    spill_array = v1751_array['spill'].astype(np.int64)
    event_array = v1751_array['event_counter'].astype(np.int64)
    board_array = v1751_array['board_id'].astype(np.int64)
    channel_array = np.array(
        [ v1751_array[v1751_channel_str_list[channel_index]].astype(np.int64)
          for channel_index in xrange(0, 5) ]
        )

    flags = (spill_array == spill) & (board_array == board+8)

    if event not in np.unique(event_array[flags]):
        print("Event {} not found".format(event))
        sys.exit(1)

    event_index = np.where(np.unique(event_array[flags]) == event)[0][0]


    fig, (ax00, ax01, ax02, ax03, ax04) = plt.subplots(5, sharex=True, sharey=True)

    axes = (ax00, ax01, ax02, ax03, ax04)

    fig.suptitle("V1751 board {} waveforms\n".format(board) +
                 "Run: {}; spill: {}; event: {}"
                 .format(run, spill, event_index))

    samples = np.arange(14336)

    for channel_index in xrange(0, 5): # The number of channels (only TOF and UT-AG)
        waveforms = channel_array[channel_index][flags]
        waveform = waveforms[event_index]
        pedestal = np.polyfit(np.arange(0,2000),waveform[0:2000],0)[0]
        pos = np.argmin(waveform)
        if (channel_index == 0):
            if waveform[pos] < (pedestal-20):
                ustof_1 = pos
            else:
                print "No signal in USTOF 1."
                ustof_1 = 0
#        if (channel_index == 1):
#            if waveform[pos] < pedestal-20:
#                ustof_2 = pos
#            else:
#                print "No signal in USTOF 2."
#                ustof_2 = 0
        if (channel_index == 2):
            if waveform[pos] < pedestal-20:
                dstof_1 = pos
            else:
                print "No signal in DSTOF 1."
                dstof_1 = 0
#        if (channel_index == 3):
#            if waveform[pos] < pedestal-20:
#                dstof_2 = pos
#            else:
#                print "No signal in DSTOF 2."
#                dstof_1 = 0
        if (channel_index == 4):
            pedestal = np.polyfit(np.arange(pos,14336),waveform[pos:14336],0)[0]
            #print pedestal
            aghit = np.sum(waveform[dstof_1-40:dstof_1+60]-pedestal)
            tof = dstof_1 - ustof_1
            #print "AG Counter Charge: ", aghit
            #print "TOF: ", tof

        """
        axes[channel_index].plot(samples, waveform, color='b')
        axes[channel_index].set_xlim([2600, 2840])
        axes[channel_index].set_ylabel("ADC count", fontsize=10)
        axes[channel_index].tick_params(axis='y', which='major', labelsize=10)
        axes[channel_index].set_title("CH{}".format(channel_index), x=1.05, y=0.25)
        """
    """
    plt.show()
    plt.close()
    """
    return aghit, tof

print '\n'
parser = argparse.ArgumentParser(description="Plot from ROOT file.")
parser.add_argument('file', type=str, help="path to ROOT file")
args = parser.parse_args()
file_path = args.file
run = parse_run(file_path).lstrip('0')

v1751_branch_list = ['spill', 'event_counter', 'trigger_time_tag', 'board_id',]
v1751_channel_str_list = [ 'channel_%s' % i for i in range(8) ]
v1751_branch_list.extend(v1751_channel_str_list)
v1751_array = rnp.root2array(file_path, 'DataQuality/v1751', v1751_branch_list)

number_entries = v1751_array.size
spill_array = v1751_array['spill'].astype(np.int64)
event_counter = v1751_array['event_counter'].astype(np.int64)
board_id = v1751_array['board_id'].astype(np.int64)
trigger_time_tag = v1751_array['trigger_time_tag']
number_spills = np.unique(spill_array).size

# Dung's morph
runNumber = int(run)
spillNumber = np.unique(spill_array)[0]
eventNumber = np.unique(event_counter)
eventCounter = len(eventNumber)
"""
print runNumber
print spillNumber
print eventNumber
print eventCounter
"""
"""
print "\nNumber of entries in file:", number_entries
print "Number of spills:", number_spills
print "Number of triggers in V1751 board 0:", trigger_time_tag[board_id == 8].size
print "Number of triggers in V1751 board 1:", trigger_time_tag[board_id == 9].size
"""
board = 0
for spill in np.unique(spill_array):
    #print "Spill: ", spill
    flags = (spill_array == spill) & (board_id == board+8)
    events = event_counter[flags]
    #print "Events: ", events
    for event in events:
        #print "event: ", event
        try:
            event_index = np.where(events == event)[0][0]
            print("V1751 board {} waveforms for run {}, spill {}, event {}. "
                  "Ctrl-C to exit.".format(board, run, spill, event_index))
            AGHit, TOF = get_event(v1751_array, board=board, run=run, spill=spill, event=event)
            print "Var 1: AGHit: ", AGHit
            print "Var 2: TOF: ", TOF
            print '\n'
        except KeyboardInterrupt:
            print "\n\nExiting..."
            sys.exit(0)
