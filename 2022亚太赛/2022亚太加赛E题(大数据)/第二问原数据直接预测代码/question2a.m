%% ���ݴ���
clc     %%��������ڵ�����
clear    %%��������ռ�����б���
Data_pro = readtable('2022_APMCM_E_Data.xlsx','Sheet', 'proliferation');
Data_cell = table2cell(Data_pro);     %%����ת��ΪԪ������
[N,M] = size(Data_cell);
Data_val = zeros(N,4);        %%����һ��N*4�������

for i=1:N                %%����ݵ�possession�е�����ȫ�����뵽���б�
    Data_val(i,1) = Data_cell{i,3};
    Data_val(i,2) = Data_cell{i,4};
    Data_val(i,3) = Data_cell{i,5};
    Data_val(i,4) = Data_cell{i,6};
end

now = Data_val(:,4);%%�������Һ�������ӵ������
perVal = 20;
perLayer = 10;

%% ģ��ѵ��
if ~exist('training_net2a.mat','file')     %�����Ƿ����training_net2a.mat��һѵ��ģ�ͣ���ͬһ���ļ���
    force=now;
    T=tonndata(force,false,false);  %��������������Ϊcell���͵ľ����Ҳ�����num2cell��ת�������ʹ�ö�άcell���󣬽��ᱻ��Ϊ����������Ӷ�����ѵ����
    trainFcn = 'trainbr';   %Ĭ�ϵ�lmh����ѵ��ʱ������Ч���ܲ���ñ�Ҷ˹�����㷨
    
    feedbackDelays = 1:perVal;    %�ӳ�����
    hiddenLayerSize = perLayer;    %%��ʾ������������ж��ٸ�
    net = narnet(feedbackDelays,hiddenLayerSize,'open',trainFcn);  %%�������Խ�ϵ�ʱ����������
    [Xs,Xi,Ai,Ts] = preparets(net,{},{},T);   %%�뿴https://www.cnblogs.com/lijinying/res/12698304.html
    net.divideParam.trainRatio = 70/100;     %%������70%������������Ŀ����������ѵ��
    net.divideParam.valRatio = 15/100;       %%15%���ڷ�ֹ�����
    net.divideParam.testRatio = 15/100;      %%15%���ڲ��ԣ�����ģ��Ľ����ʵ�ʵĽ��֮������
    net = train(net,Xs,Ts,Xi,Ai);   %%Ȼ��Ļ�����net��preparentsת��������ݽ���ѵ�����м��ԭ�������˵����Ҫ�ǲ����������
    view(net);
    save('training_net2a.mat','net');     %%����ѵ����ģ�͵�������
end

%% Ԥ��
net = importdata('training_net2a.mat');    %%����ģ��
PreYear = 130-perVal;
len = length(now);
res = zeros(1,len+perVal);    %Ԥ�������
%ǰperVal����Ԥ��ֱ�����ֳɵ�
res(1:perVal)= now(1:perVal);
for i=1:len-perVal       %������perVal��׼ȷ��Ԥ����һ��,Ԥ���ȥ�Ľ�����ϣ���һ��Ч��
    ytest = num2cell(now(i:i + perVal)');  %%�뿴https://blog.csdn.net/jk_101/article/details/110929630
    [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);%%�����ȴ������ݳɶ�Ӧ������
    temp1 = net(AA,AB,AC);    %%Ȼ�����ѵ��
    res(i+perVal) = temp1{1};     %%�����ݷŽ�ȥ
end
p2 = res;

for i=1:PreYear     %����Ԥ�������Ҳ���ظ�֮ǰ�Ĳ���
    ytest = num2cell(res(len+i-perVal-1:len+i-1));
    [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);
    temp1 = net(AA,AB,AC);
    res(i+len) = temp1{1};
    p2(i+len) = ceil(res(i+len));
end

%% ��ʾԤ����
sy = Data_val(1,1);
X_p_1 = [sy:1:sy+len-1];%%����ԭʼ���ݵ�x��
X_p_2 = [sy:1:sy+length(res)-1];%%����Ԥ���x��
figure(2)
hold on
plot(X_p_1,now,'r');
plot(X_p_2,res,'b--');
legend({'real value','predictive value'});
title('Number of nuclear weapon states in the world')