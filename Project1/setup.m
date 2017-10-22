%% setup.m
%  Function to connect to Turtlebot hardware.
%   Arguments:
%   - ip: Either host IP, or IP of VM running Gazebo.
%   - turtlebot: Name of the turtlebot you are intending to use, if any.

function setup(ip, turtlebot)
    rosshutdown; % terminate any existing nodes
    switch nargin
        case 1
            % No Turtlebot name given - assume we're connecting to Gazebo
            rosinit(ip);
        case 2
            % Assume connecting to hardware since Turtlebot name specified
            turtlebotIp = sprintf('%s.neu.edu', turtlebot);
            rosinit(turtlebotIp, 'NodeHost', ip); 
    end
           
end