<h1>Maximum point quadratic function</h1>
<h2>Determined with genetic algorithm</h2>
<img src='https://github.com/w-i-l/maximum-point-quadratic-function/assets/65015373/b603eca8-26ad-445f-afca-052eaa3b8d34'>



<br>
<hr>
<h2>About it</h2>
<p>This project finds the maximum value for a given quadratic function using the genetics algorithms.</p>
<p>It provides both a <code>cli</code> and <code> gui</code> and outputs all the intermediary steps in the process.</p>
<p>While the scope of this projects is to find the maximum point of a quadratic function, the algorithm can be used for any other function, by changing the <code>codification</code> method and the <code>fitness</code> function.</p>


<br>
<hr>
<h2>How to use it</h2>
<p>For this project there are some dependencies that must be installed. You can opt for having a <a href="https://docs.python.org/3/library/venv.html">virtual environment</a> for managing them, case in which you have to run this snippet:</p>

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

<p>After that, by running the the code you would have to choose which interface you want the project to be run in.</p>
<p>For the <code>cli</code> you have to manually adjust the parameters from the <a href="https://github.com/w-i-l/maximum-point-quadratic-function/blob/main/src/main.py">main</a> before running the app. In the <code>graphic interface</code>, the parameters can be change at the runtime.</p>


<br>
<hr>
<h2>How it works</h2>
<p>The algorithm first need all the parameters set, which are:</p>
<ul>
    <li><code>population_size: int</code> - how big the population will be</li>
    <li><code>generations: int</code> - for how many generations the app will run</li>
    <li><code>lower_bound: float</code> - lower bound for <b>x</b> values</li>
    <li><code>upper_bound: float</code> - upper bound for <b>x</b> values</li>
    <li><code>precision: int</code> - how many digits for floating representation</li>
    <li><code>function arguments: list[float]</code> - the coefficients for the quadratic function</li>
    <li><code>combination_rate: float</code> - the probability for combining two cromosomes (from 0 to 1)</li>
    <li><code>mutation_rate: float</code> - the probability for a cromosome to mutate (from 0 to 1)</li>
</ul>

<p>For generating the next generation, the algorithm uses the following steps:</p>

> **_NOTE:_** That to have a maximum point in a quadratic function, the first coefficient must be negative.

<h3>Codification</h3>
<p>For the genetic algorithm to work, the cromosomes must be codified in a way that the algorithm can understand. In this case, the cromosomes are represented as a list of <b>binary</b> values, where each value represents a bit of the <b>x</b> value. The number of bits is determined by the <code>precision</code> parameter.</p>
<p>For a given <code>precision</code> the algorithm will need</p>

$$ \lceil \log2((\text{upper\_bound} - \text{lower\_bound}) \times 10^{\text{precision}}) \rceil $$

<p>bits to represent the <b>x</b> value in binary.</p>
<p>For a more information about encoding and decoding check this: <a href="https://cms.fmi.unibuc.ro/problem/genetici1">resource</a>.</p>
<hr/>

<h3>Selection</h3>
<p>For the selection process, the algorithm uses the <a href="https://en.wikipedia.org/wiki/Selection_(genetic_algorithm)#Elitist_Selection">elitist selection</a> method. This method selects the best cromosomes from the current population and propagate it to the next generation.</p>
<hr/>

<h3>Crossover</h3>
<p>The crossover process is done by selecting pairs of cromosomes from the current population and combining them to create two new cromosomes. The probability for this to happen is determined by the <code>combination_rate</code> parameter. The best cromosome from the current generation is excluded from this process.</p>
<p>The combination reffers to chosing a single point from the binary represenattion and swapping the values from that point.</p>
<hr/>

<h3>Mutation</h3>
<p>The mutation process is done by selecting cromosomes from the current population and changing a random bit from it. The probability for this to happen is determined by the <code>mutation_rate</code> parameter.</p>

<br>
<hr>
<h2>Tech specs</h2>
<p>The graphical interface is made using <a href="https://docs.python.org/3/library/tkinter.html">tkinter</a> and the <code>graph</code> 
<p>The <code>GUI</code> provides 4 buttons:</p>
<ul>
    <li><code>Next</code> - it iterates a generation and updates all labels</li>
    <li><code>Auto</code> - it iterates all generation until it is stopped and updates all labels</li>
    <li><code>Reset</code> - creates a new population with the saved inputs and starts again from generation 1</li>
    <li><code>Go to generation</code> - jump to a given generation without updating the labels</li>
</ul>

<p>The app features a menu <code>settings</code> tab from which all parameters can be changed.</p>

> **_NOTE:_** It is a very computationally expensive process, so it is not recommended to use a big population size or a big number of generations. This only affects the big jumps made with the <code>Go to generation</code> button.

<p>The app is not using a reactive framework. All the updates are done using <code>__update</code> prefixed methods.</p>