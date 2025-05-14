# CITS55505 GROUP 54 Project

## Introduction

Our project is a recipe recording app called SmartBite. It is a personal food analytics companion, designed to help you monitor your dietary habits with precision. By uploading your daily meals, you can track calorie intake, protein intake, and nutritional quality over time. Our intelligent system provides instant feedback and tailored insights to support your health and fitness goals, whether you're aiming to lose weight, build muscle, or simply eat more mindfully.

Upload your meal data effortlessly through our user-friendly interface. Visualize your eating patterns with dynamic charts and graphs that highlight trends and potential areas for improvement. Share your progress securely with friends, nutritionists and stay motivated together! SmartBite empowers you to turn everyday eating into meaningful, measurable progress toward a healthier lifestyle.

## Team

| UWA ID   | Name        | GitHub Username                |
| -------- | ----------- | ------------------------------ |
| 24690471 | Songwen You | @swyou                         |
| 22853272 | Simon Li    | @simonli66666 and @XihengLi666 |
| 23746283 | Harry Zheng | @arryzheng                     |
| 24565925 | Jue Hou     | @chuck20011002                 |


## Environment & Development 

### Prerequisites
- **Python >= 3.9**

### Setup environment
#### 1. Clone the Repository
```
git clone git@github.com:swyou/CITS5505-G54.git
cd CITS5505-G54
```

#### 2. Set up python environment
```
python -m venv venv 
```

#### 3. Activate virtual environment:
For **Windows**:
```
venv\Scripts\activate

```

For Linux/MacOS
```
source venv/bin/activate
```

#### 4. Install requirements
```
pip install -r requirements.txt

```

#### 5. Run App
```bash
python run.py
```

#### 6. Run Tests

- Run unit tests

```bash
python -m unittest tests.unit_tests
```



- Run selenium tests

```bash
python -m unittest tests.selenium
```




### Git related

#### 1. Create a Feature Branch  

```bash
git checkout -b feature/some-new-feature
```

#### 2. Commit Changes
```bash
git commit -m "Some descriptive commit message here"
```

#### 3. Push and Create Pull Request
```bash
git push origin feature/some-new-feature
```
   - Then open a Pull Request describing the changes and referencing any relevant issues.