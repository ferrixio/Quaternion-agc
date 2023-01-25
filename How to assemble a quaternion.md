# How to assemble a quaternion

🐉 Author: Samuele Ferri (@ferrixio)

## Basic construction

A quaternion can be defined in the _standard_ way using integers, floats, lists or tuples. The main constructor has five (optional) arguments:

+ **real**: a float, pre-initialized to 0, representing the real part;
+ **i_img**: a float, pre-initialized to 0, representing the first imaginary part;
+ **j_img**: a float, pre-initialized to 0, representing the second imaginary part;
+ **k_img**: a float, pre-initialized to 0, representing the third imaginary part;
+ **seq**: a list or tuple, pre-initialized to None, representing the components of the quaternion.

The "pre-constructor" `__new__` checks if the arguments in input are valid, else an error will raise.

After the object is constructed, it will only have one attribute in the `self` variable, called `q`, representing the list of the four components of the quaternion.

To get its principal elements, five properties were added:

+ **real**, to get the real part
+ **i_img**, to get the first imaginary part;
+ **j_img**, to get the second imaginary part;
+ **k_img**, to get the third imaginary part;
+ **norm**, to get the euclidean norm of the quaternion as 4D-vector.

### From a complex number

It is possible to build a quaternion from a complex number, using the classmethod `from_complex`. It takes in input a complex number and an optional string representing which quaternionic-imaginary part the complex-j represents.

### Using random()

With this method, three numbers between 0 and 1 are randomly generated. Then, the quaternion is setted to be unitary.
To avoid floating point accuracy, the procedure repeats the generation until it gets an unitary quaternion. 

### Using randint()

Similar to the previous one, this method generates a quaternion whose components are random integers. Those numbers are in range -50 to 50, but the user can extend (o reduce) these bounds.