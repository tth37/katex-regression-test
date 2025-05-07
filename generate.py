import os
import json
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("OPENAI_MODEL")
api_base = os.getenv("OPENAI_API_BASE")
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url=api_base,
)


def generate_test_cases(num_cases=50):
    prompt = """Generate a Markdown paragraph that mixes regular text with LaTeX mathematical expressions. 
Use a variety of LaTeX delimiters:
- Inline math: $...$ or \\(...\\)
- Display math: $$...$$ or \\[...\\]
- Chemical equations: \\ce{...}
- Physical units: \\pu{...}
- Equation environments: \\begin{equation}...\\end{equation}

Make the content complex with:
- Multiple math expressions per paragraph
- Math expressions at start/end of paragraphs
- Different delimiter types in same paragraph
- Complex mathematical notation
- To test the robustness of the parser, you can randomly include some errors:
  - Missing closing delimiters
  - Missing whitespaces between delimiters and regular text

DO NOT use Chinese, Japanese, or Korean characters.

Example format:

The quadratic formula$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$ solves equations of form \\[ax^2 + bx + c = 0\\]. 
For \\ce{H2O}, molar mass is \\pu{18.015 g/mol}. Consider:
\\begin{equation}
\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}
\\end{equation}


Now generate 1 new unique paragraph:"""

    test_cases = []

    for i in range(num_cases):
        print(f"Generating case {i+1}/{num_cases}")
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates Markdown with LaTeX content.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )

            content = response.choices[0].message.content.strip()
            test_cases.append(content)

        except Exception as e:
            print(f"Error generating case {i+1}: {str(e)}")
            continue

    return test_cases


if __name__ == "__main__":
    test_cases = generate_test_cases(50)

    # Save to JSON file
    with open("test-cases.json", "w") as f:
        json.dump(test_cases, f, indent=2)

    print(f"Successfully generated {len(test_cases)} test cases in test-cases.json")
