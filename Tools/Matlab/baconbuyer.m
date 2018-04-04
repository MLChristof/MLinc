%% Initialization
tic

clear all; close all; clc;

%% Input

Choose_GUI = 1;

if Choose_GUI
    filename  = uipickfiles('num',1,...
        'Output','char',...
        'FilterSpec', 'C:\Data\Documents\Christof\Matlab\Trading\Hackathon',...
        'type',{'*.csv', 'CSV'});
    
else
    filename = 'C:\Data\Documents\Christof\Matlab\Trading\Hackathon\1D\Majors1\EURAUD1440.csv';
end

data = import_trade_data(filename);

filterpar = 100;

L = filter(ones(filterpar,1)/filterpar,1,data.high_dat(:));
L_diff = gradient(L);
L_bend = gradient(L_diff);
L_diff_sign = sign(L_diff);
L_bend_sign = sign(L_bend);
L_diff_sign_change = L_diff_sign(1:end-1)~=L_diff_sign(2:end);
idx = find(L_diff_sign_change);
idx_low = find(L_bend(idx)>0);
idx_low = idx(idx_low);
idx_high = find(L_bend(idx)<0);
idx_high = idx(idx_high);
prctile_low = prctile(L_bend(idx_low),50);
prctile_high = prctile(L_bend(idx_high),50);
idx_low = find(L_bend(idx)>prctile_low);
idx_low = idx(idx_low);
idx_high = find(L_bend(idx)<prctile_high);
idx_high = idx(idx_high);

% sig_low = (sign(L_diff(idx_low-2))==-1 & sign(L_diff(idx_low-1))==-1 & sign(L_diff(idx_low+1))==1 & sign(L_diff(idx_low+2))==1);
% sig_high = (sign(L_diff(idx_high-2))==1 & sign(L_diff(idx_high-1))==1 & sign(L_diff(idx_high+1))==-1 & sign(L_diff(idx_high+2))==-1);
% idx_low = idx_low(sig_low);
% idx_high = idx_high(sig_high);

x_vec1 = 1:length(L);
x_vec2 = 1:length(L_diff);
x_vec3 = 1:length(L_bend);
figure
plot(x_vec1,L)
hold on
plot(x_vec1(idx_low),L(idx_low),'ro')
plot(x_vec1(idx_high),L(idx_high),'go')
figure
plot(x_vec2,L_diff)
hold on
plot(x_vec2(idx_low),L_diff(idx_low),'ro')
plot(x_vec2(idx_high),L_diff(idx_high),'go')