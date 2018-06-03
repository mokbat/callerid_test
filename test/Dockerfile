FROM python
COPY requirements.txt .
COPY test_functional.py .
COPY test_load.py .
COPY logger.py .

COPY CallerIDTestPlan.rst .
COPY EndToEndTestStrategy.rst .

RUN pip3 install --no-cache-dir -r requirements.txt
