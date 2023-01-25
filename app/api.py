import uvicorn
import json
from fastapi import FastAPI, HTTPException

app = FastAPI(title='shop.kz API')


with open('../smartphones.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


@app.get('/', tags=['Home Page'])
async def get_home_page():
    """
    This is the Home Page
    """
    return {'message', 'This is the Home Page. To see all supported links go to /docs or /redoc'}


@app.get('/smartphones', tags=['Smartphones price'])
async def read_item(price: str):
    """
    Return smartphone information if the price equals
    """
    result = [item for item in data if item['price'] == price]
    if not result:
        return HTTPException(status_code=404, detail=f"price with value '{price}' wasn't found")
    return result


if __name__ == '__main__':
    uvicorn.run(app)
