class EC2Error(Exception):
    # Base class for EC2 related errors
    pass


class InstanceCreateError(EC2Error):
    def __init__(self, error):
        super().__init__(f"Faild to create instance: {error}")


class NoInstanceFoundById(EC2Error):
    def __init__(self, id):
        super().__init__(f"No instance found with id: {id}")


class InstanceNotMatchingTags(EC2Error):
    def __init__(self, tags_to_match):
        super().__init__(f"Instance must have tags: {tags_to_match}")


class NoRunningInstancesError(EC2Error):
    def __init__(self):
        super().__init__(f"There are no running instances.")


class RunningInstanceCountLimitReached(EC2Error):
    def __init__(self, max_instances):
        super().__init__(
            f"Running instance limit reached, there can only be {max_instances} instances running."
        )


class InstanceAlreadyInState(EC2Error):
    def __init__(self, state):
        super().__init__(f"Instance is already in {state} state.")


class InstanceTypeError(EC2Error):
    def __init__(self, available_instance_types):
        super().__init__(
            f"Invalid instance type, types can only be: {available_instance_types}"
        )


class AMITypeError(EC2Error):
    def __init__(self, available_image_types):
        super().__init__(
            f"Invalid AMI type, types can only be: {available_image_types}"
        )
