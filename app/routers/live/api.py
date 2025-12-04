from fastapi import APIRouter, WebSocketDisconnect ,WebSocket, Query ,Path
from fastapi.responses import StreamingResponse
import asyncio ,glob ,re ,os,json,requests,logging
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Optional




router = APIRouter()



# 遍歷數字list
def extract_number(filename):
    nums = re.findall(r'\d+',os.path.basename(filename))
    print(nums)
    return int(nums[0]) if nums else -1


# 時間轉換
class TZFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, tz=None):
        super().__init__(fmt=fmt, datefmt=datefmt)
        self.tz = tz or ZoneInfo("UTC")

    def converter(self, timestamp):
        # 把 timestamp 轉成指定時區的 datetime
        dt = datetime.fromtimestamp(timestamp, self.tz)
        return dt.timetuple()


# 取得今天日期（Asia/Taipei 時區）
# now = datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y%m%d")
# log_path = f'/app/log/{now}_socket.log'
# handler = logging.FileHandler(log_path, encoding='utf-8')
# formatter = TZFormatter(fmt="%(asctime)s - %(levelname)s - %(message)s", tz=ZoneInfo("Asia/Taipei"))
# handler.setFormatter(formatter)
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# logger.addHandler(handler)



# 撰寫websocket channel
@router.websocket("/ws/data")
async def websocket_winddata(websocket: WebSocket):
    
    origin = websocket.headers.get("origin")
    client_ip = websocket.headers.get("x-forwarded-for") or websocket.client.host
    # logger.info(f'來自 {client_ip} 的使用者已啟動環境因子即時推送服務')


    print(f"WebSocket 連線 Origin: {origin}, IP: {client_ip}", flush=True)

    allowed_origins = ["http://localhost","http://221.120.5.217:5174","http://192.168.1.66:5174", None, ""]  # 放寬允許 None 和空字串
    
    if origin not in allowed_origins:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    # logger.info(f'成功建立來自 {client_ip} 的 WebSocket 連線')
    print(f'Client connected: {client_ip}', flush=True)

    try:
        while True:
            path = '/app/parameters/'
            files = glob.glob(f'{path}*.txt')

            if not files:
                msg = {"error":"No .txt files found"}
            else:
                latest_file = max(files,key=extract_number)
                data = {}

                try:
                    with open(latest_file,'r',encoding='cp950') as f_lines:
                        for line in f_lines:
                            if '=' in line:
                                key , value = line.strip().split('=',1)
                                data[key.strip()] = value.strip()
                    msg = data
                except Exception as e:
                    error_msg = f"Failed to read file: {str(e)}"
                    msg = {"error": error_msg}
                    # logger.error(f"[{client_ip}] {error_msg}")

            await websocket.send_text(json.dumps(msg,ensure_ascii=False))
            await asyncio.sleep(eval(os.getenv('Push_Time')))

    except WebSocketDisconnect:
        print("WebSocket 客戶端斷開連線")
        # logger.info(f'來自 {client_ip} 的使用者已中斷連線並離開推送通道')

    except Exception as e:
        print(f"WebSocket 發生錯誤：{e}")
        
    finally:
        try:
            await websocket.close()
            
        except Exception:
            pass


def iter_bytes(response):
  for chunk in response.iter_content(chunk_size=1024):   
    if isinstance(chunk, bytes):
      yield chunk
    else:
      yield str(chunk).encode()


 # 兼容windows及linux
if not os.path.exists('/.dockerenv'):
    from dotenv import load_dotenv
    load_dotenv()



# 串流攝影機
@router.get("/stream/{dimension}")
def proxy_stream(
    dimension: str = Path(..., description="維度參數: 2d , 3d"),
    Width: Optional[int] = Query(None, description="若需要，請輸入寬度"),
    Height: Optional[int] = Query(None, description="若需要，請輸入高度")
):  
    
    ip = os.getenv('PublicIP')
    if dimension == '2d':
        input_url = f"http://{ip}:8086/getimage?Width={Width}&Height={Height}"
        default_url = f"http://{ip}:8086/getimage?Width=1920&Height=1080"
        
    elif dimension == '3d':
        input_url = f"http://{ip}:8035/getimage?Width={Width}&Height={Height}"
        default_url = f"http://{ip}:8035/getimage?Width=1920&Height=1080"
       
    else:
        return StreamingResponse(iter([b"Dimension must be '2d' or '3d'"]), media_type="text/plain")

    url = input_url if Width and Height else default_url
    auth = ("admin", "Pass1234")

    try:
        r = requests.get(url, auth=auth, stream=True, timeout=10)
        media_type = r.headers.get('Content-Type', 'multipart/x-mixed-replace')
        return StreamingResponse(iter_bytes(r), media_type=media_type)
    except Exception as e:
        # 回傳錯誤訊息作為流
        error_msg = f"Stream error: {e}".encode()
        return StreamingResponse(iter([error_msg]), media_type="text/plain")
    
