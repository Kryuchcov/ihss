#include <ros/ros.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <std_msgs/Int32.h>
#include <std_msgs/String.h>

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;
ros::Publisher pub;

void go_to_pose(float x, float w)
{
  std_msgs::String msg;
	msg.data="wait";
  pub.publish(msg);
  //tell the action client that we want to spin a thread by default
  MoveBaseClient ac("move_base", true);
  printf("going to %f %f\n",x,w);

  //wait for the action server to come up
  while(!ac.waitForServer(ros::Duration(5.0)))
  {
    ROS_INFO("Waiting for the move_base action server to come up");
  }

  move_base_msgs::MoveBaseGoal goal;

  //we'll send a goal to the robot to move 1 meter forward
  goal.target_pose.header.frame_id = "map";
  goal.target_pose.header.stamp = ros::Time::now();

  goal.target_pose.pose.position.x= x;
  goal.target_pose.pose.position.y= w;
  goal.target_pose.pose.orientation.w= 0.5;

  ROS_INFO("Sending goal");
  ac.sendGoal(goal);

  ac.waitForResult();
  /*while (ac.waitForResult())
  {
    msg.data="wait";
    pub.publish(msg);
  }*/

  if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
  {
    ROS_INFO("Hooray, the base moved 1 meter forward");
    msg.data="succeded";
   	pub.publish(msg);
  }
  else
  {
    ROS_INFO("The base failed to move forward 1 meter for some reason");
    msg.data="failed";
		pub.publish(msg);
  }
}

void callback(const std_msgs::Int32::ConstPtr& zone)
{
  //decido a donde tengo que ir
  /* 1=cocina
     2=sala
     3=recamara
     4=punto inicial (comedor)*/

  switch (zone->data)
  {
    case 1:
              printf("cocina \n");
              go_to_pose(3.81,14.3);
              break;
    case 2:
              printf("sala \n");
              go_to_pose(6.41,15.5);
              break;
    case 3:
              printf("recamara \n");
              go_to_pose(9.36,15.9);
              break;
    case 4:
              printf("comedor \n");
              go_to_pose(2.99,15.3);
              break;
    default:
              printf("no existe la zona\n");
              break;
  }
}




int main(int argc, char** argv)
{
  ros::init(argc,argv,"simple_navigation_goals");
  ros::NodeHandle n;
  ros::Subscriber sub=n.subscribe("robot_go_to",1,callback);
  pub=n.advertise<std_msgs::String>("robot_goal_status",1);

  ros::spin();
}
