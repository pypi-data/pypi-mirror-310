from chat2edit import (ChatCycle, ChatMessage, ContextMessage, ExecutionResult,
                       FunctionMessageFeedback, PromptCycle, PromptingResult)

IMAGE_EDITING_VI_EXEMPLARS = [
    ChatCycle(
        req_message=ChatMessage(text=""),
        request=ContextMessage(
            text="Hãy xóa con chó khỏi bức ảnh",
            objs_or_paths=["image0"],
        ),
        prompt_cycles=[
            PromptCycle(
                prompting_result=PromptingResult(
                    messages=[
                        "_",
                        (
                            "thinking: We need find the dog first before we can remove it.\n"
                            "commands:\n"
                            'dogs = find_image_objects_by_label(image0, label="dog")'
                        ),
                    ],
                    code='dogs = find_image_objects_by_label(image0, label="dog")',
                ),
                execution_result=ExecutionResult(
                    blocks=['dogs = find_image_objects_by_label(image0, prompt="dog")'],
                    feedback=FunctionMessageFeedback(
                        severity="warning",
                        text="Found 2 image objects with the label `dog`.",
                        objs_or_paths=["annotated_image0_0"],
                    ),
                ),
            ),
            PromptCycle(
                prompting_result=PromptingResult(
                    messages=[
                        "_",
                        (
                            "thinking: The system detected two image objects with the label `dog` along with the annotated image. We need to display the annotated image and ask the user to specify which object should be removed.\n"
                            "commands:\n"
                            'response_to_user(text="Trong ảnh có 2 con chó, bạn muốn chọn con nào để xóa?", variables=[annotated_image0_0])'
                        ),
                    ],
                    code='response_to_user(text="Trong ảnh có 2 con chó, bạn muốn chọn con nào để xóa?", variables=[annotated_image0_0])',
                ),
                execution_result=ExecutionResult(
                    blocks=[
                        'response_to_user(text="Trong ảnh có 2 con chó, bạn muốn chọn con nào để xóa?", variables=[annotated_image0_0])'
                    ],
                    response=ContextMessage(
                        text="Trong ảnh có 2 con chó, bạn muốn chọn con nào để xóa?",
                        objs_or_paths=["annotated_image0_0"],
                    ),
                ),
            ),
        ],
    ),
]

IMAGE_EDITING_EN_EXEMPLARS = [
    ChatCycle(
        req_message=ChatMessage(text=""),
        request=ContextMessage(
            text="Please remove the dog from the photo.", objs_or_paths=["image0"]
        ),
        prompt_cycles=[
            PromptCycle(
                prompting_result=PromptingResult(
                    messages=[
                        "_",
                        (
                            "thinking: We need to find the dog first before we can remove it.\n"
                            "commands:\n"
                            'dogs = find_image_objects_by_label(image0, label="dog")'
                        ),
                    ],
                    code='dogs = find_image_objects_by_label(image0, label="dog")',
                ),
                execution_result=ExecutionResult(
                    blocks=['dogs = find_image_objects_by_label(image0, prompt="dog")'],
                    feedback=FunctionMessageFeedback(
                        severity="warning",
                        text="Found 2 image objects with the label `dog`.",
                        objs_or_paths=["annotated_image0_0"],
                    ),
                ),
            ),
            PromptCycle(
                prompting_result=PromptingResult(
                    messages=[
                        "_",
                        (
                            "thinking: The system detected two image objects with the label `dog` along with the annotated image. We need to display the annotated image and ask the user to specify which object should be removed.\n"
                            "commands:\n"
                            'response_to_user(text="There are 2 dogs in the image. Which one would you like to remove?", variables=[annotated_dog_image])'
                        ),
                    ],
                    code='response_to_user(text="There are 2 dogs in the image. Which one would you like to remove?", variables=[annotated_image0_0])',
                ),
                execution_result=ExecutionResult(
                    blocks=[
                        'response_to_user(text="There are 2 dogs in the image. Which one would you like to remove?", variables=[annotated_image0_0])'
                    ],
                    response=ContextMessage(
                        text="There are 2 dogs in the image. Which one would you like to remove?",
                        objs_or_paths=["annotated_image0_0"],
                    ),
                ),
            ),
        ],
    ),
]
