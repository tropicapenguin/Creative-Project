/*
  Feeding experimentation device 3 (FED3)
  Creativity Project Code
  For the automated feeder. With the task of being the initializer for the Experiement through a nose poke.

  rgerritsen@uiowa.edu
  October, 2022

*/

#include <FED3.h>                //Include the FED3 library 
String sketch = "Creative";       //Unique identifier text for each sketch
FED3 fed3 (sketch);              //Start the FED3 object

//variables for PR tasks
int interaction = false;                                       // this variable is the number of pokes since last pellet

void setup() {
  fed3.begin();                                         //Setup the FED3 hardware
}

void loop() {
  fed3.run();
  if (interaction == false) {
    if (fed3.Left) {                                    //If left poke
      fed3.logLeftPoke();                               //Log left poke and reset the boolean of fed3.Left
      fed3.ConditionedStimulus(1);                      //Deliver conditioned stimulus (tone and lights)
      fed3.BNC(25, 0.5);                                  //Deliver 1 pulses at 25Hz (25ms HIGH, 25ms LOW), lasting 1 second
      interaction = true;                                     //setting the respond to 1 to prevent repeated response
      //fed3.Left = false;
    }
    if (fed3.Right) {                            //If right poke is triggered
      fed3.logRightPoke();                              //Log Right Poke and reset the boolean of fed3.Right
      fed3.ConditionedStimulus(1);                      //Deliver conditioned stimulus (tone and lights)
      fed3.BNC(25, 0.5);
      interaction = true;
      //fed3.Right = false;
    }
  } else {
    fed3.ReadBNC(true);
    if (fed3.BNCinput) {
      interaction = false;                                     // success in trial reset response
      fed3.Feed();
      fed3.Timeout(2);                                  //Time out for 3 seconds to allow the trial to reset
    }
  }
  fed3.UpdateDisplay();
}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                    Call fed.run at least once per loop
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
