import anki_vector
import time
from anki_vector.util import degrees, distance_mm, speed_mmps, Pose
from anki_vector.events import Events

import functools
import threading
import sys

cube_pose = Pose(x=0,y=0,z=0, angle_z = degrees(0))
observed_event = threading.Event()
moved_event = threading.Event()

def on_oo(event_type, event):
	if (event.object_family == 3):
		observed_event.set()
		
def on_om(event_type, event):
	moved_event.set()


def main():
	with anki_vector.Robot(requires_behavior_control=True) as robot:
		
		try:
			while True:
				robot.behavior.set_eye_color(0.0,1.0)
				robot.anim.play_animation('anim_eyepose_furious')
				
				robot.events.subscribe(on_oo, Events.robot_observed_object)
				robot.say_text("WHERE IS MY CUBE?", duration_scalar=0.5)
				robot.behavior.set_head_angle(degrees(0))
				observed_event.clear()
				while not observed_event.wait(timeout=0.4):
					robot.behavior.turn_in_place(degrees(22.5), accel = degrees(5000), speed = degrees(5000))
				robot.events.unsubscribe(on_oo, Events.robot_observed_object)
	
				robot.world.connect_cube()
				robot.behavior.dock_with_cube(robot.world.connected_light_cube,num_retries=3)
				robot.say_text("GOTCHA!", duration_scalar = 0.6)
				robot.behavior.set_lift_height(1.0, accel = 255, max_speed = 255)
				robot.behavior.set_lift_height(0, accel = 255, max_speed = 255)
				moved_event.clear()
				robot.events.subscribe(on_om, Events.object_moved)
				while not moved_event.wait():
					robot.events.unsubscribe(on_om, Events.object_moved)
		except KeyboardInterrupt:
			sys.exit()
			
if __name__ == '__main__':
	main()