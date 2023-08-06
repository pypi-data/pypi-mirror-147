import math

def hwone():
  Scrap_Precent_1 = None # Scrap precent 1
  Scrap_Precent_2 = None # Scrap precent 2
  Scrap_Precent_3 = None # Scrap Precent 3
  Parts_Required = None# Part Required
  Shift_Length = None# Shift Lenght
  Part_Time = None # Part TIme
  Reliability_Precentage = None# Reliability Precentage
  Efficency_Precentage = None# Efficency Precentage
  Produce_Num_Parts = None # Produce Number parts
  Final_num_machines = None # Final_num_machinesinal Number of machiens

  Error = "" #Error Message if invalid type is entered



  # These while loops are error checking, they check to make sure that a value was submited
  # Then that the value is less than 100 (because its a whole number precent) and
  # is greater than a zero value meaning that a negative precent cant be used
  # If any of those issues exist it rempromts the user to enter the value before heading
  # to the next input. This process is roughly similar for all. There is also a type error
  # exception that refuses the abiitity for a user to break the function by using text
  # and even incorporates an error message.

  # Scrap Precent 1
  while(Scrap_Precent_1 == None or Scrap_Precent_1 > 100 or Scrap_Precent_1 < 0):
      print(Error)
      print("What is the Scrap Precent for step 1? (Enter a number 0-100)")
      try:
          Scrap_Precent_1 = float(input()) / 100 # Convert Value to a precent
          #    print(str(Scrap_Precent_1)) # Debug output and veryify value
      except ValueError:
          Error = "Please Enter as a number "
  Error = "" # Clear Error error message


  # Scrap Precent 2
  while(Scrap_Precent_2 == None or Scrap_Precent_2 > 100 or Scrap_Precent_2 < 0):
      print(Error)
      print("What is the Scrap Precent for step 1? (Enter a number 0-100)")
      try:
          Scrap_Precent_2 = float(input()) / 100 # Convert Value to a precent
          #    print(str(Scrap_Precent_2)) # Debug output and veryify value
      except ValueError:
          Error = "Please Enter as a number "
  Error = ""


  # Scrap Precent 2
  while(Scrap_Precent_3 == None or Scrap_Precent_3 > 100 or Scrap_Precent_3 < 0):
      print(Error)
      print("What is the Scrap Precent for step 3? (Enter a number 0-100)")
      try:
          Scrap_Precent_3 = float(input()) / 100 # Convert Value to a precent
          #    print(str(Scrap_Precent_3)) # Debug output and veryify value
      except ValueError:
          Error = "Please Enter as a number "
  Error = ""


  # Parts Required
  while(Parts_Required == None or Parts_Required < 0):
      print(Error)
      print("What is the number of good parts out required for step 3 per shift?")
      try:
          Parts_Required = int(input())
      #   print(str(Parts_Required)) # Debug output and veryify value
      except ValueError:
          Error = "Please Enter as a number "
  Error = ""


  # Part Time
  while(Part_Time == None or Part_Time < 0):
      print(Error)
      print("What is the standard time per part in hours? ")
      try:
          Part_Time = float(input())
      #   print(str(Parts_Required)) # Debug output and veryify value
      except ValueError:
          Error = "Please Enter as a number "
  Error = ""
  #    print(str(Part_Time)) # Debug output and veryify value


  # Shift Length
  while(Shift_Length == None or Shift_Length < 0):
      print(Error)
      print("How long is a shift in hours?")
      try:
          Shift_Length = float(input())
      #   print(str(Shift_Length)) # Debug output and veryify value
      except ValueError:
          Error = "Please Enter as a number "
  Error = ""


  # Reliability Percent
  while(Reliability_Precentage == None or Reliability_Precentage < 0 or Reliability_Precentage > 100):
      print(Error)
      print("What is the Reliability percent, Enter the number (0-100)")
      try:
          Reliability_Precentage = int(input()) / 100 # Convert Value to a precent
      #    print(str(Reliability_Precentage)) # Debug output and veryify value
      except ValueError:
          Error = "Please Enter as a number "
  Error = ""


  # Efficency Precent
  while(Efficency_Precentage == None or Efficency_Precentage < 0 or Efficency_Precentage > 100):
      print(Error)
      print("What is the Efficency Precentage , Enter the number (0-100)")
      try:
          Efficency_Precentage = int(input()) / 100 # Convert Value to a precent
      #    print(str(Efficency_Precentage))  # Debug output and veryify value
      except ValueError:
          Error = "Please Enter as a number "
  Error = ""



  # First Equation
  Produce_Num_Parts = Parts_Required / ( ( 1- Scrap_Precent_1) *  (1- Scrap_Precent_2)  *  (1- Scrap_Precent_3))


  #print("Totals Parnts Needed: " + str(Produce_Num_Parts)) # Debug output and veryify value
  #Produce_Num_Parts = Parts_Required / ( 1- Scrap_Precent_1) # Debug output and veryify value
  #  SQ / EShift_Length Final_num_machinesunction


  # Second Equation
  Final_num_machines = (Part_Time * Produce_Num_Parts) / ( Reliability_Precentage * Efficency_Precentage * Shift_Length )

  print ("Final_num_machinesractional Parts Needed is: " + str(round(Final_num_machines,2)))
  print("Total Machines Needed is: " + str(math.ceil(Final_num_machines)))


def hwtwo():

  Val = [None]*5 # Define Array (create an array with 5 null elements)

  # user Input Prompt. This prompts the user to input data based off the passed
  # prompt argument, then checks if the value is a string if it is, it errors out.
  # if not a strong it countines back to the top of the while loop and checks
  # if the value was set and if the value is greater than one, if both are true
  # it returns the input value, this value is stored as a float.
  def Userinput(Prompt):
      input_val = None
      while input_val == None or input_val < 0: # If the values is less than zero,or undefiend
          print(Prompt) # Ask the user a # QUESTION:
          try:
              input_val = float(input()) # Attempt to get input
              if input_val < 0: # If the value was below zero print error message
                  print("ERROR: Please enter a input value that is positve")
                  print("")
          except ValueError:# If the input was as string print error message
              print("ERROR: Value Was a string)")
      return input_val


  # Create the average of the array values. This is done but summing all elements
  #in the array and then deviding by the number of elements in the array.
  def AverageCalc(Array):
      sum = 0
      for x in Array: # Add of the elements in the array together
          sum = sum + x
      return sum / len(Array) # Devide by the number of elements in the array

  # Get all 5 User Inputs, this is a basic loop to truncate the expression a bit
  i = 0
  while (i < 5):
      #print(i)
      # We have to connocate the string here because if we want to pass this information to the print fuction
      Val[i] = Userinput(f"What is the measured value for the item {i+1} in the sample?")
      i = i + 1

  # Get the Other two user data points.
  GoalAvg = Userinput("What is the goal Average Value? ")
  GoalStdev = Userinput("What is the goal standard deviation value? ")
  # Add in some white space
  print("")



  #lower bound formula. Take the users goal standard Deviation, and there goal Average
  # And create he boundrys for the Calcuated range.
  Bound = (( 3 * GoalStdev) / math.sqrt(len(Val)))
  #print(Bound) # Debug Print the Boundry element
  LowerBound = GoalAvg - Bound
  UpperBound = GoalAvg + Bound

  # Calculate average / mean of the dataset.
  CalAverage = AverageCalc(Val)
  #print(CalAverage) #Debug Print the Calcuated average

  # Print out the Boundrys along with the values.
  print("Lower Bound:  " + str(round(LowerBound,2)))
  print("Calcuated Average:  " + str(round(CalAverage,2)))
  print("Upper Bound:  " + str(round(UpperBound,2)))
  print("") # Whitespace

  if LowerBound < CalAverage < UpperBound:
      print("Passed: the acutal average is within the tolerance range")

  elif CalAverage > UpperBound:
      print("Warning: the actual average is ABOVE the tolerance range")
  elif CalAverage < LowerBound:
      print("Warning: the actual average is LOWER the tolerance range")
  else:
      print("Warning: the actual average is not within the tolerance range")
