from tqdm.asyncio import tqdm_asyncio
import asyncio
import sys
import asyncio
import random
from tqdm.asyncio import tqdm

async def async_get_questions():
    # middle_df,fee = get_question_csv_from_content(task_type, content ,name)
    # df = pd.concat([df,middle_df])
    # num = num + 1
    # total_fee = total_fee + fee
    await asyncio.sleep(10)
    
async def async_main():
    tasks=[async_get_questions() for _ in range(10)]
    _ = [await task_ for task_ in tqdm.as_completed(tasks, total=len(tasks))]

async def task():
    await asyncio.sleep(0.5 + random.random()) # <- await + something that's awaitable
    # adding random val to prevent it finishing altogether,
    # or progress bar will seemingly jump from 0 to 100 again.


async def main():
    tasks = [task() for _ in range(10)]
    _ = [await task_ for task_ in tqdm.as_completed(tasks, total=len(tasks))]


asyncio.run(main())