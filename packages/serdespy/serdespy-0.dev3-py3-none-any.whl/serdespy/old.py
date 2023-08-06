# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 19:08:42 2022

@author: richa
"""
def four_port_to_diff_old(network, port_def, terminate = True):
    """Genterates PRBS31 sequence

    Parameters
    ----------
    network : skrf Network
        4 port network object
        example: 
            s4p_file = 'path/to/touchstonefile.s4p'
            network = rf.Network(s4p_file)
    
    port_def: 2*2 array
        defines TX and RX side ports of network
        example:
            port_def = np.array([[TX1_index, RX1_index],[TX2_index, RX2_index]])
            
            PORT DEFINITIONS: 
                Port   1  ----->  TX Side      G11     RX Side  <-----  Port   2
                Port   3  ----->  TX Side      G12     RX Side  <-----  Port   4
                
            port_def = np.array([[0, 1],[2, 3]])

    Returns
    -------
    H : array
        tranfer function of differential channel
    
    f : array
        frequency vector
        
    h : array
        impulse response
    
    t = array
        time vector
        
    """
    #TODO: add options for termination and source impedance
    
    #define all in-out subnetworks and ABCD params for those networks
    
    
    #thru networks
    ch1_thru = rf.subnetwork(network, [port_def[0][0], port_def[0][1]])
    ch1_thru_abcd = rf.s2a(ch1_thru.s)

    ch2_thru = rf.subnetwork(network, [port_def[1][0], port_def[1][1]])
    ch2_thru_abcd = rf.s2a(ch2_thru.s)
    
    
    #xtalk networks
    tx1_rx2 = rf.subnetwork(network, [port_def[0][0], port_def[1][1]])
    tx1_rx2_abcd = rf.s2a(tx1_rx2.s)
    
    tx2_rx1 = rf.subnetwork(network, [port_def[0][1], port_def[1][0]])
    tx2_rx1_abcd = rf.s2a(tx2_rx1.s)

    #add termination to match charictaristic impedance of networks 12 and 34
    if terminate:
        source1 = impedance(ch1_thru.z0[:,0])       
        term1 = admittance(1/ch1_thru.z0[:,0])
        
        ch1_thru_abcd = series(source1, ch1_thru_abcd)
        ch1_thru_abcd = series(ch1_thru_abcd,term1)

        source2 = impedance(ch2_thru.z0[:,0])   
        term2 = admittance(1/ch2_thru.z0[:,0])
        
        ch2_thru_abcd = series(source2, ch2_thru_abcd)
        ch2_thru_abcd = series(ch2_thru_abcd,term2)
    
        source_tx1_rx2 = impedance(tx1_rx2.z0[:,0])  
        tx2_rx1_abcd = series(source_tx1_rx2, tx2_rx1_abcd)
        
        source_tx2_rx1 = impedance(tx1_rx2.z0[:,0])
        tx2_rx1_abcd = series(source_tx2_rx1, tx2_rx1_abcd)
        
        
    #get discrete transfer function for subnetworks, assuming 0 source impedance
    H1_thru = 1/ch1_thru_abcd[:,0,0]
    H2_thru = 1/ch2_thru_abcd[:,0,0]
    H_tx1_rx2 = 1/tx1_rx2_abcd[:,0,0]
    H_tx2_rx1 = 1/tx2_rx1_abcd[:,0,0]

    #Get discrete transfer function of differential signal
    H = (H1_thru + H2_thru - H_tx2_rx1 - H_tx1_rx2)/2
    
    H = H/H[0]
    
    #Get frequency response of differential transfer function
    f = network.f
    h, t = freq2impulse(H,f)
      
    return H, f, h, t

    def CTLE(self, b,a,f):
                
        """Behavioural model of continuous-time linear equalizer (CTLE). Input signal is self.signal, this method modifies self.signal
    
        Parameters
        ----------
        
        b: array
            coefficients in numerator of ctle transfer function
        a: array
            coefficients in denomenator of ctle transfer function
    
        """
            
        #create freqency vector in rad/s
        w = f/(2*np.pi)
        
        #compute Frequency response of CTLE at frequencies in w vector
        w, H_ctle = sp.signal.freqs(b, a, w)
        
        #convert to impulse response
        h_ctle, t_ctle = freq2impulse(H_ctle,f)
        
        #check that time_steps match
        if ((t_ctle[1]-self.t_step)/self.t_step>1e-9):
            print("Invalid f vector, need length(f)/f[1] = ", self.t_step)
            return False
        
        #convolve signal with impulse response of CTLE
        signal_out = sp.signal.fftconvolve(self.signal, h_ctle[:100], mode = 'same')
        
        self.signal = np.copy(signal_out)
        
def nrz_input(samples_per_symbol, data_in, voltage_levels):
    
    """Genterates  ideal, square, NRZ (PAM-2) transmitter waveform from binary sequence

    Parameters
    ----------
    samples_per_symbol: int
        timesteps per bit
    
    length: int
        length of desired time-domain signal
    
    data_in: array
        binary sequence to input, must be longer than than length/samples_per_symbol
    
    voltage levels: array
        definition of voltages corresponding to 0 and 1. 
        voltage_levels[0] = voltage corresponding to 0 bit, 
        voltage_levels[1] = voltage corresponding to 1 bit
    
    length: float
        timestep of time domain signal
    
    Returns
    -------
    signal: array
        square waveform at trasmitter corresponding to data_in

    """
    
    signal = np.zeros(samples_per_symbol*data_in.size)
    
    for i in range(data_in.size):
        if (data_in[i] == 0):
            signal[i*samples_per_symbol:(i+1)*samples_per_symbol] = np.ones(samples_per_symbol)*voltage_levels[0]
        elif(data_in[i] == 1):
            signal[i*samples_per_symbol:(i+1)*samples_per_symbol]  = np.ones(samples_per_symbol)*voltage_levels[1]
        else:
            print('unexpected symbol in data_in')
            return False
            
        #if (i%100000 == 0):
         #   print('i=',i)
    
    return signal

def pam4_decision(x,voltage_levels):
    l = (voltage_levels[0]+voltage_levels[1])/2
    m = (voltage_levels[1]+voltage_levels[2])/2
    h = (voltage_levels[2]+voltage_levels[3])/2
    
    if x<l:
        return 0
    elif x<m:
        return 1
    elif x<h:
        return 2
    else:
        return 3

def nrz_decision(x,voltage_levels):
    threshold = (voltage_levels[0]+voltage_levels[1])/2
    if x<threshold:
        return 0
    else:
        return 1

    def oversample(self, samples_per_symbol):
        
        """Oversamples the baud-rate-sampled signal

        Parameters
        ----------
        
        samples_per_symbol : int
            number of samples per symbol
            
        
        """
        self.samples_per_symbol = samples_per_symbol
        
        #if we have FIR filtered data
        if self.FIR_enable:
            oversampled = np.zeros(len(self.signal_FIR_BR)*self.samples_per_symbol)
            for i in range(self.n_symbols):
                oversampled[i*self.samples_per_symbol:(i+1)*self.samples_per_symbol]=self.signal_FIR_BR[i]
        
        #if we are not using FIR
        else:
            oversampled = np.zeros(len(self.signal_BR)*self.samples_per_symbol)
            for i in range(self.n_symbols):
                oversampled[i*self.samples_per_symbol:(i+1)*self.samples_per_symbol]=self.signal_BR[i]
        
        self.signal_ideal = oversampled
def pam4_input(samples_per_symbol, data_in, voltage_levels):
    
    """Genterates ideal, square, PAM-4 transmitter waveform from binary sequence

    Parameters
    ----------
    samples_per_symbol: int
        timesteps per bit
    
    length: int
        length of desired time-domain signal
    
    data_in: array
        quaternary sequence to input, must be longer than than length/samples_per_symbol
    
    voltage levels: array
        definition of voltages corresponding to symbols. 
        voltage_levels[0] = voltage corresponding to 0 symbol, 
        voltage_levels[1] = voltage corresponding to 1 symbol
        voltage_levels[2] = voltage corresponding to 2 symbol
        voltage_levels[3] = voltage corresponding to 3 symbol
    
    length: float
        timestep of time domain signal
    
    Returns
    -------
    signal: array
        square waveform at trasmitter corresponding to data_in

    """
    
    signal = np.zeros(samples_per_symbol*data_in.size)
    
    for i in range(data_in.size):
        if (data_in[i]==0):
            signal[i*samples_per_symbol:(i+1)*samples_per_symbol] = np.ones(samples_per_symbol)*voltage_levels[0]
        elif (data_in[i]==1):
            signal[i*samples_per_symbol:(i+1)*samples_per_symbol] = np.ones(samples_per_symbol)*voltage_levels[1]
        elif (data_in[i]==2):
            signal[i*samples_per_symbol:(i+1)*samples_per_symbol] = np.ones(samples_per_symbol)*voltage_levels[2]
        elif (data_in[i]==3):
            signal[i*samples_per_symbol:(i+1)*samples_per_symbol] = np.ones(samples_per_symbol)*voltage_levels[3]
        else:
            print('unexpected symbol in data_in')
            return False

        if (i%100000 == 0):
            print('i=',i)
    
    return signal