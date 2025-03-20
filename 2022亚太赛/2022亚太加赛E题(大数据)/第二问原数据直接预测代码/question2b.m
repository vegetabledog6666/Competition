%% ���ݴ���
clc
clear
Data_test = readtable('2022_APMCM_E_Data.xlsx','Sheet', 'stockpiles');
Data_cell = table2cell(Data_test);
%���ұ�ǩתΪ���ֱ��
ContryLabel = Data_cell(:,1);
ContryLabel_cat = categorical(ContryLabel);    %%������һ��categorical���͵����飬Ϊ��������
ContryLabel_int = double(ContryLabel_cat);
TotalContryNum = size(unique(ContryLabel_int),1);   %%ȥ��Ȼ��ͳ�ƹ�����
[N,M] = size(Data_cell);

TotalYear = 78;
CountrysStocks = zeros(TotalContryNum+1,TotalYear);   %%��ʾ����һ���Թ���Ϊ�б�ǩ��ʱ��Ϊ�б�ǩ�ı�
for i= 1:N
    CountrysStocks(ContryLabel_int(i),Data_cell{i,3}-1944) = Data_cell{i,4};   %%ͳ��ÿ������ÿһ��ĺ�����
end
for i=1:TotalYear   %%ͳ�ƺ���������
    CountrysStocks(TotalContryNum+1,i) = sum(CountrysStocks(1:TotalContryNum,i));
end
%% Ԥ���������������ͬʱҲԤ��ȫ������������������ʹ��
data = CountrysStocks(TotalContryNum+1,:)';  %%ȡ���һ��
perVal = 24;
perLayer = 12;
perVal2 = [12,21,24,10,22,18,10,12,10,10];
perLayer2 = [8,10,10,10,10,10,10,10,10,10];
%% ģ��ѵ��
if ~exist('training_net2bgloabl.mat','file')  %%��ȫ�����������ģ��ѵ��
    net = MyTrainNet(data,perVal,perLayer);
    save('training_net2bgloabl.mat','net');
end


for i=1:TotalContryNum    %%ÿ�����ҽ���ѵ��
    if ~exist(['training_net2b',num2str(i), '.mat' ],'file')
        data0 = CountrysStocks(i,1:78)';%%��ÿ�����ҵĺ�����Ū����
        net2 = MyTrainNet(data0,perVal2(i),perLayer2(i));  %%����ģ��ѵ��
        save(['training_net2b',num2str(i), '.mat' ],'net2');%%�����Ӧ��ѵ��ģ��
    end
end

%% Ԥ��
net = importdata('training_net2bgloabl.mat');
PreYear = 130-perVal;

[p,p2] = MyPerdict(net,data,perVal,PreYear);%%�ȶ��ܵĽ���Ԥ�⣬p�������ں�δ����p2����δ���ģ����߶���ʾ����������
p_conutry = zeros(TotalContryNum,length(p));    %%����������*��Ԥ��+��ȥ����ݵı�
nets = cell(TotalContryNum,1);
for i=1:TotalContryNum
    net2 = importdata(['training_net2b',num2str(i), '.mat' ]);  %%�����Ӧ��ģ��
    nets{i} = net2;     %%����ÿ�����Ҷ�Ӧѵ����������
    data0 = CountrysStocks(i,:)';    %%����ÿ�����ҵĺ���������
    [pp,pp2] = MyPerdict(net2,data0,perVal,PreYear);
    p_conutry(i,:) = pp2;     %%�������ÿ������δ����Ԥ��ֵ
end
len0 = length(data0);

for j=1:PreYear             %%����Ļ���������
    tempVal = zeros(TotalContryNum,1);    %%��ʱ���������ʾ
    for i = 1:TotalContryNum
        data2 = p_conutry(i,len0+j-perVal-1:len0+j-1);
        p3 = MyPerdict2(nets{i},data2,perVal);
        tempVal(i,1) = p3;
    end
    tempTotal = sum(tempVal);
    for i = 1:TotalContryNum
        p_conutry(i,len0 + j) = 0.25*tempVal(i,1)/tempTotal*p2(len0+j)+0.75*p_conutry(i,len0 + j);
    end
    
end


%% ��ͼչʾ

figure(1)
X_p = [1945:1:2022];    %%����ԭ����ͼ��
X_p_2 = [1945:1:1945+length(p)-1];    %%����������δ��

for i=1:TotalContryNum   
    subplot(2,5,i)
    Y_p = CountrysStocks(i,:);
    plot(X_p,Y_p,'r')   %%�����������ʵֵ
    hold on
    pp2 = p_conutry(i,:);     %%����������Ԥ��ֵ
    plot(X_p_2,pp2,'b--');
    axis([min(X_p),max(X_p_2),0,max([max(Y_p),max(pp2)])]);
    xlabel('year');
    ylabel('stockpile');
    contrySTR = find(ContryLabel_int == i);
    legend({'��ʵֵ','Ԥ��ֵ'});
    title(ContryLabel{contrySTR(1)})
end


%% ����
function net = MyTrainNet(data,perVal,perLayer)
    force=data;
    T=tonndata(force,false,false);  %��������������Ϊcell���͵ľ����Ҳ�����num2cell��ת�������ʹ�ö�άcell���󣬽��ᱻ��Ϊ����������Ӷ�����ѵ��?
    trainFcn = 'trainbr';   %Ĭ�ϵ�lmh����ѵ��ʱ������Ч���ܲ���ñ�Ҷ˹�����㛎

    feedbackDelays = 1:perVal;    %�ӳ�����
    hiddenLayerSize = perLayer;   %%���ز�����
    net = narnet(feedbackDelays,hiddenLayerSize,'open',trainFcn);   %%�����������Իع�������
    [Xs,Xi,Ai,Ts] = preparets(net,{},{},T);       %%����Ԥ����
    net.divideParam.trainRatio = 70/100;
    net.divideParam.valRatio = 15/100;      %%�����������趨
    net.divideParam.testRatio = 15/100;
    net = train(net,Xs,Ts,Xi,Ai);      %%����ѵ��
    view(net);
end

function [p,p2] = MyPerdict(net,data,perVal,PreYear)%%������ܵ�Ԥ��
    len = length(data);    
    p = zeros(1,len+perVal);
    p2 = p;      
    p(1:perVal)= data(1:perVal);       %ǰperVal����Ԥ��ֱ�����ֳɵģ��������˼�������1��24
    for i=1:len-perVal     %������perVal��׼ȷ��ֵԤ����һ��
        ytest = num2cell(data(i:i + perVal)');   %%��һ�����ݾ���ǰ����Ѿ�Ԥ�����ʱ����Ԥ��
        [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);    %%���ݳ�ʼ��
        temp1 = net(AA,AB,AC);     %%����������
        p(i+perVal) = temp1{1};      
        p2(i+perVal) = round(p(i+perVal)*0.15 + data(i+perVal)*0.85); 
    end
    %p2 = round(p);
    if PreYear>0
        for i=1:PreYear
            %����Ԥ�����
            ytest = num2cell(p(len+i-perVal-1:len+i-1));  %%len֮���������len֮ǰ�����ݽ���Ԥ��
            [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);
            temp1 = net(AA,AB,AC);
            p(i+len) = temp1{1};
            p2(i+len) = ceil(p(i+len));
        end
    end
end

function p3 = MyPerdict2(net,data2,perVal)
    ytest = num2cell(data2);
    [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);    %%��������Ԥ����
    temp1 = net(AA,AB,AC);   %%������ѵ��
    p3 = ceil(temp1{1});
end
