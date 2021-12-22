import rospy
from actionlib import SimpleActionClient
from smach import StateMachine, Concurrence, State
import smach_ros
from custom_ros_action.msg import InitDroneAction, InitDroneGoal, InitDroneResult, InitDroneAction, MoveAgentAction, MoveAgentGoal


if __name__ == '__main__':
    rospy.init_node('pid_action_client')

    sm = StateMachine(outcomes=['succeeded', 'aborted', 'preempted'])
    with sm:
        StateMachine.add(label='CONNECT', 
                        state=smach_ros.SimpleActionState('init_drone', InitDroneAction, goal=InitDroneGoal(type='connect')),
                        transitions={'succeeded': 'CON'},
                        )
        # StateMachine.add(label='TAKEOFF', 
        #                 state=smach_ros.SimpleActionState('init_drone', InitDroneAction, goal=InitDroneGoal(type='takeoff')),
        #                 transitions={'succeeded': 'MANUAL'},
        #                 )
        # StateMachine.add(label='MANUAL',
        #                 state=smach_ros.SimpleActionState('manual_control', MoveAgentAction),
        #                 transitions={'aborted': 'LAND', 'succeeded':'PID'}
        #                 )

        """Concurrent & Nested"""
        sm_concurrent = Concurrence(outcomes=['succeeded', 'aborted'],
                                    default_outcome='succeeded',
                                    outcome_map={'aborted': {'PUBLISH':'aborted'}})
    
        # sm_nested = StateMachine(outcomes=['succeeded', 'aborted', 'preempted'])
        # with sm_nested:
        #     StateMachine.add('SEARCH',
        #                     state=smach_ros.SimpleActionState('search_executor', MoveAgentAction),
        #                     transitions={'aborted': 'TRACK',
        #                                  'succeeded': 'SEARCH'}
        #                     )
        #     StateMachine.add('TRACK',
        #                     state=smach_ros.SimpleActionState('track_executor', MoveAgentAction),
        #                     transitions={'aborted': 'SEARCH',
        #                                  'succeeded': 'TRACK'}
        #                     )
                                    
        # Open the container
        with sm_concurrent:
            Concurrence.add('PUBLISH', state=smach_ros.SimpleActionState('mode_switcher', InitDroneAction))
            Concurrence.add('CONTROL_MOTOR', state=smach_ros.SimpleActionState('controller', InitDroneAction))

        StateMachine.add('CON', sm_concurrent,
                        transitions={'succeeded':'CON',
                                            'aborted':'aborted'}
                        )

    # Execute SMACH plan
    outcome = sm.execute()
      