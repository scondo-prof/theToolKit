FROM public.ecr.aws/lambda/python:3.12.2024.03.22.11-x86_64

# Copy function code and any necessary files to the container
# COPY royomartin_parser/lambda_function.py ${LAMBDA_TASK_ROOT}
COPY cwLogsEventFilterSet/lambda_function.py ${LAMBDA_TASK_ROOT}
COPY cwLogsEventFilterSet/cw_logs_data.py ${LAMBDA_TASK_ROOT}
COPY cwLogsEventFilterSet/requirements.txt .

# Install any function dependencies
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile) 
CMD [ "lambda_function.lambda_handler" ]