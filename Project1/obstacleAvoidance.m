%% obstacleAvoidance
%  Script to navigate to a specified goal destination, avoiding obstacles.

%% Setup 
gains = struct('goalTargeting', 100, 'forwardPath', 0, ...
                'continuousPath', 0, 'obstacleAvoid', 100);

% Init publishers and subscribers
timerHandles.pub = rospublisher('/mobile_base/commands/velocity');
timerHandles.pubmsg = rosmessage('geometry_msgs/Twist');

timerHandles.sublaser = rossubscriber('/scan');
timerHandles.subodom = rossubscriber('/odom');
timerHandles.subbump = rossubscriber('/mobile_base/sensors/bumper_pointcloud');

% Reset Odometry
odomresetpub = rospublisher('/mobile_base/commands/reset_odometry');  
odomresetmsg = rosmessage('std_msgs/Empty');
send(odomresetpub,odomresetmsg)
pause(2);    % wait until reset

% Add gains to timerHandles
timerHandles.gains = gains;

timer1 = timer('TimerFcn',{@exampleHelperTurtleBotObstacleTimer,timerHandles},'Period',0.1,'ExecutionMode','fixedSpacing');
timer1.StopFcn = {@exampleHelperTurtleBotStopCallback};


%% Run VFH Algorithm

start(timer1);
while strcmp(timer1.Running, 'on')
  exampleHelperTurtleBotShowGrid(timerHandles.sublaser);
  pause(0.5);
end

delete(timerfindall);




                