# ehire-51job

该脚本可根据年龄、关键词过滤简历，再通过ChatGPT对简历进行进一步的筛选，并且对通过筛选的候选人打招呼。

## Installation

`pip install -r requirements.txt`

## Usage

1. 配置好 _params.json_ 和 _.env_
2. `python main.py`
3. 手动在打开的浏览器中登录前程无忧

## Documentation

* params.json：配置职位名称和要求，注意职位名称需要与开放的职位完全一致。
* .env：配置OPENAI_API_KEY，也支持自定义OPENAI_BASE_URL

## Running Tests

TODO

## License

MIT License