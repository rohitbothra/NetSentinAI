import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

class BaseAgent:
    def __init__(self, name, model="gemini-1.5-flash", system_instruction=""):
        self.name = name
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = model
        self.system_instruction = system_instruction
        self.chat_history = []

    def log(self, message):
        print(f"[{self.name}] {message}")

class ForensicsAgent(BaseAgent):
    def __init__(self, tools):
        super().__init__(
            name="ForensicsAgent", 
            system_instruction="""
            You are a Network Forensics Expert. 
            Your goal is to analyze traffic logs to find specific evidence of attacks.
            You have access to tools to read PCAP files and check IP reputations.
            Always use your tools before guessing.
            """
        )
        self.tools = tools

    def analyze(self, user_request):
        self.log("Starting investigation...")
        
        # We manually register tools for this agent
        response = self.client.models.generate_content(
            model=self.model,
            contents=user_request,
            config=types.GenerateContentConfig(
                tools=[self.tools.read_pcap_summary, self.tools.check_ip_reputation],
                system_instruction=self.system_instruction
            )
        )
        
        # Handle Tool Calls (Simple Loop)
        if response.function_calls:
            for call in response.function_calls:
                fname = call.name
                args = call.args
                self.log(f"Calling function: {fname} with {args}")
                
                # Execute the tool
                if fname == "read_pcap_summary":
                    result = self.tools.read_pcap_summary(**args)
                elif fname == "check_ip_reputation":
                    result = self.tools.check_ip_reputation(**args)
                else:
                    result = "Error: Unknown tool"

                # Send result back to Gemini
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[
                        types.Content(role="user", parts=[types.Part(text=user_request)]),
                        types.Content(role="model", parts=response.candidates[0].content.parts),
                        types.Content(role="user", parts=[
                            types.Part.from_function_response(name=fname, response={"result": result})
                        ])
                    ]
                )

        return response.text

class TopologyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TopologyAgent",
            system_instruction="""
            You are a Network Infrastructure Expert.
            Your job is to look at network diagram images and identify physical devices, 
            connections, and potential bottlenecks or misconfigurations.
            """
        )

    def analyze_image(self, image_path, prompt):
        self.log(f"Analyzing visual topology: {image_path}...")
        try:
            image = Image.open(image_path)
            response = self.client.models.generate_content(
                model=self.model,
                contents=[self.system_instruction, image, prompt]
            )
            return response.text
        except Exception as e:
            return f"Error analyzing image: {e}"

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Orchestrator",
            system_instruction="You are the Incident Commander. You coordinate other agents to solve security tickets."
        )
    
    def synthesize(self, forensics_report, topology_report):
        self.log("Synthesizing final Root Cause Analysis...")
        prompt = f"""
        Combine these two reports into a final executive summary.
        
        REPORT A (Forensics): {forensics_report}
        REPORT B (Topology): {topology_report}
        
        Output format:
        1. Executive Summary
        2. Technical Root Cause
        3. Recommended Remediation
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text