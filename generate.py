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
- Equation environments: \\begin{equation}...\\end{equation}

Make the content complex with:
- Multiple math expressions per paragraph
- Math expressions at start/end of paragraphs
- Different delimiter types in same paragraph
- Complex mathematical notation

PLEASE WRITE REGULAR TEXT using Chinese, Japanese, or Korean.

Example format:

在数学中，$E=mc^2$是一个著名的方程式。\\[ \\int_0^1 x^2 \\, dx = \\frac{1}{3} \\]这个方程描述了能量和质量之间的关系。\\ce{H2O}是水的化学式。
数学の世界では、$a^2 + b^2 = c^2$という有名な方程式があります、\\[ \\sum_{i=1}^{n} i = \\frac{n(n+1)}{2} \\]これは自然数の和を表しています。\\ce{CO2}は二酸化炭素の化学式で。
수학에서, $\\frac{a}{b} = c$는 비율을 나타내는 유명한 방정식입니다.\\[ \\sqrt{x^2 + y^2} = z \\]이 방정식은 피타고라스의 정리를 설명합니다.\\ce{NaCl}은 소금의 화학식이며.


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
    test_cases = generate_test_cases(20)

    # Save to JSON file
    with open("test-cases-cjk.json", "w", encoding='utf-8') as f:
        json.dump(test_cases, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated {len(test_cases)} test cases in test-cases.json")
