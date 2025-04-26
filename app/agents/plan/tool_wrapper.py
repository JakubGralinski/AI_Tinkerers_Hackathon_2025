from agents import Runner

class Tool:
    def __init__(self, name, description, agent, run_func=None):
        self.name = name
        self.description = description
        self.agent = agent
        self.run_func = run_func

    async def run(self, input_text):
        if self.run_func:
            return await self.run_func(self.agent, input_text)
        else:
            task = Runner.run(self.agent, input_text)
            result = await task
            return result.final_output