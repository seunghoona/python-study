from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import jwt

# jwt 설치
# pip install pyjwt

# 시크릿 키와 알고리즘 설정
SECRET_KEY = "your_secret_key"  # JWT를 인코딩/디코딩할 때 사용할 시크릿 키
ALGORITHM = "HS256"  # JWT 인코딩에 사용할 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 액세스 토큰의 만료 시간(분 단위)

# OAuth2PasswordBearer 인스턴스 생성
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # 토큰 URL 설정

# 사용자 데이터베이스 시뮬레이션
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedpassword",  # 해시된 비밀번호
        "disabled": False,
    }
}


# 사용자 모델 정의
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str  # 데이터베이스에 저장된 해시된 비밀번호


# 사용자 인증 함수
def authenticate_user(fake_db, username: str, password: str):
    """
    사용자 인증을 수행하는 함수.
    :param fake_db: 사용자 데이터베이스
    :param username: 사용자 이름
    :param password: 사용자 비밀번호
    :return: 인증된 사용자 객체 또는 False
    """
    user = fake_db.get(username)
    if not user:
        return False
    if user["hashed_password"] != password:
        return False
    return UserInDB(**user)


# 토큰 생성 함수
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    JWT 액세스 토큰을 생성하는 함수.
    :param data: 토큰에 포함할 데이터
    :param expires_delta: 토큰 만료 시간
    :return: 인코딩된 JWT 토큰
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 현재 사용자 가져오기
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    현재 인증된 사용자를 가져오는 함수.
    :param token: OAuth2 토큰
    :return: 인증된 사용자 객체
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return User(**user)
