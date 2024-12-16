# XR-AI-Backend Setup

## Create python virtual environment

``` sh
python3 -m venv .venv
```

## Activate virtual environment

### For Mac

``` sh
source .venv/bin/activate
```

### For Window

``` sh
.venv\Scripts\activate
```

## Install / update required package from file requirements.txt
### Install
``` sh
pip install -r requirements.txt
```
### Update
```sh
pip freeze > requirements.txt
```
## Run project
```sh
uvicorn app.main:app --reload
```
# Project Structure
```
.  
├── app  
│   ├── api         // các file api được đặt trong này  
│   ├── core        // chứa file config load các biến env & function tạo/verify JWT access-token 
│   ├── helpers     // các function hỗ trợ như login_manager, paging  
│   ├── models      // Database model, tích hợp với alembic để auto generate migration  
│   ├── schemas     // Pydantic Schema (custom request and response for api)  
│   ├── services    // Chứa logic CRUD giao tiếp với DB  
│   └── main.py     // cấu hình chính của toàn bộ project  
├── .gitignore  
├── env.example  
├── logging.ini     // cấu hình logging  
├── README.md  
└── requirements.txt    // file chứa các thư viện để cài đặt qua pip install
```