%% trackAndFollow
%  Script to find, track and follow a blue ball for 30s.  

%% Setup 

handles.colorImgSub = exampleHelperTurtleBotEnableColorCamera;
handles.cliffSub = rossubscriber('/mobile_base/events/cliff', 'BufferSize', 5);
handles.bumpSub = rossubscriber('/mobile_base/sensors/bumper_pointcloud', 'BufferSize', 5);
handles.soundPub = rospublisher('/mobile_base/commands/sound', 'kobuki_msgs/Sound');
handles.velPub = rospublisher('/mobile_base/commands/velocity');

blueBallParams.blueMax = 30; % Maximum permissible deviation from pure blue
blueBallParams.darkMin = 90; % Minimum acceptable darkness value
latestImg = readImage(handles.colorImgSub.LatestMessage);
[c,~,ball] = exampleHelperTurtleBotFindBlueBall(latestImg,blueBallParams);
exampleHelperTurtleBotPlotObject(latestImg,ball,c);
pause(3);

handles.params = blueBallParams;

gains.lin = struct('pgain',1/100,'dgain',1/1000,'igain',0,'maxwindup',0','setpoint',0.75);
gains.ang = struct('pgain',1/100,'dgain',1/3000,'igain',0,'maxwindup',0','setpoint',0.5);

handles.gains = gains;

timer2 = timer('TimerFcn',{@exampleHelperTurtleBotTrackingTimer,handles},'Period',0.1,'ExecutionMode','fixedSpacing');

%% Run Tracking Algorithm

start(timer2);
pause(30);

delete(timerfindall);