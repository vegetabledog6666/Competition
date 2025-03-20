%% 数据处理
clc     %%清理命令窗口的内容
clear    %%清除工作空间的所有变量
Data_pro = readtable('2022_APMCM_E_Data.xlsx','Sheet', 'proliferation');
Data_cell = table2cell(Data_pro);     %%将表转化为元胞数组
[N,M] = size(Data_cell);
Data_val = zeros(N,4);        %%返回一个N*4的零矩阵

for i=1:N                %%将年份到possession中的内容全部打入到新列表
    Data_val(i,1) = Data_cell{i,3};
    Data_val(i,2) = Data_cell{i,4};
    Data_val(i,3) = Data_cell{i,5};
    Data_val(i,4) = Data_cell{i,6};
end

now = Data_val(:,4);%%各个国家核武器的拥有数量
perVal = 20;
perLayer = 10;

%% 模型训练
if ~exist('training_net2a.mat','file')     %代表是否存在training_net2a.mat这一训练模型，从同一个文件夹
    force=now;
    T=tonndata(force,false,false);  %输入和输出矩阵须为cell类型的矩阵，且不能用num2cell来转换，如果使用二维cell矩阵，将会被认为是两个输入从而不能训练。
    trainFcn = 'trainbr';   %默认的lmh函数训练时间序列效果很差，采用贝叶斯正则化算法
    
    feedbackDelays = 1:perVal;    %延迟向量
    hiddenLayerSize = perLayer;    %%表示隐含层的数量有多少个
    net = narnet(feedbackDelays,hiddenLayerSize,'open',trainFcn);  %%非线性自结合的时间序列网络
    [Xs,Xi,Ai,Ts] = preparets(net,{},{},T);   %%请看https://www.cnblogs.com/lijinying/res/12698304.html
    net.divideParam.trainRatio = 70/100;     %%代表有70%的输入向量与目标向量用于训练
    net.divideParam.valRatio = 15/100;       %%15%用于防止过拟合
    net.divideParam.testRatio = 15/100;      %%15%用于测试，测试模拟的结果与实际的结果之间的误差
    net = train(net,Xs,Ts,Xi,Ai);   %%然后的话就用net对preparents转化后的数据进行训练，中间的原理后面再说，主要是不断修正误差
    view(net);
    save('training_net2a.mat','net');     %%保存训练的模型到这里面
end

%% 预测
net = importdata('training_net2a.mat');    %%读入模型
PreYear = 130-perVal;
len = length(now);
res = zeros(1,len+perVal);    %预测的数据
%前perVal个不预测直接用现成的
res(1:perVal)= now(1:perVal);
for i=1:len-perVal       %依次用perVal个准确的预测下一个,预测过去的进行拟合，试一下效果
    ytest = num2cell(now(i:i + perVal)');  %%请看https://blog.csdn.net/jk_101/article/details/110929630
    [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);%%还是先处理数据成对应的向量
    temp1 = net(AA,AB,AC);    %%然后进行训练
    res(i+perVal) = temp1{1};     %%把数据放进去
end
p2 = res;

for i=1:PreYear     %迭代预测后续，也是重复之前的步骤
    ytest = num2cell(res(len+i-perVal-1:len+i-1));
    [AA,AB,AC] = preparets(net,{},{},[ytest(perVal) ytest]);
    temp1 = net(AA,AB,AC);
    res(i+len) = temp1{1};
    p2(i+len) = ceil(res(i+len));
end

%% 显示预测结果
sy = Data_val(1,1);
X_p_1 = [sy:1:sy+len-1];%%这是原始数据的x轴
X_p_2 = [sy:1:sy+length(res)-1];%%这是预测的x轴
figure(2)
hold on
plot(X_p_1,now,'r');
plot(X_p_2,res,'b--');
legend({'real value','predictive value'});
title('Number of nuclear weapon states in the world')