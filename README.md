# CITS55505 GROUP 54 Project

## Introduction

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

#### 4. Install flask
```
pip install Flask

```

#### 5. Other
According to `Flask` file structure, static html files are expected in `app/static/` directory.


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