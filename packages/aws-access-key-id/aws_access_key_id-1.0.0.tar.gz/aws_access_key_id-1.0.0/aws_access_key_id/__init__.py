import json


def get_resource_type(prefix):
    """Return the resource type based on the prefix."""
    prefix_to_type = {
        "ABIA": "AWS STS service bearer token",
        "ACCA": "Context-specific credential",
        "AGPA": "Group",
        "AIDA": "IAM user",
        "AIPA": "Amazon EC2 instance profile",
        "AKIA": "Access key",
        "ANPA": "Managed policy",
        "ANVA": "Version in a managed policy",
        "APKA": "Public key",
        "AROA": "Role",
        "ASCA": "Certificate",
        "ASIA": "Temporary (AWS STS) keys",
    }
    return prefix_to_type.get(prefix, "Unknown resource type")


def aws_account_from_aws_key_id(aws_key_id):
    """Decode AWS Key ID to get the associated AWS account ID."""
    if len(aws_key_id) <= 4:
        return "Invalid Key ID"
    trimmed_key_id = aws_key_id[4:]  # Remove the first 4 characters
    decoded = base32_decode(trimmed_key_id)
    y = decoded[:6]
    z = int.from_bytes(y, byteorder="big")
    mask = 0x7FFFFFFFFF80
    e = (z & mask) >> 7
    return str(e).zfill(12)  # Return 12-digit account ID


def base32_decode(input_str):
    """Decode a base32-encoded string."""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    buffer = 0
    bits_left = 0
    output = bytearray()
    for char in input_str:
        val = alphabet.find(char.upper())
        if val == -1:
            continue  # Skip invalid characters
        buffer = (buffer << 5) | val
        bits_left += 5

        if bits_left >= 8:
            bits_left -= 8
            output.append(buffer >> bits_left)
            buffer &= (1 << bits_left) - 1

    return bytes(output)


def aws_access_key_id(aws_access_key_id):
    """Extract AWS account ID and resource type from an AWS access key ID."""
    try:
        # Validate input
        if not aws_access_key_id or len(aws_access_key_id) < 4:
            raise ValueError("Invalid AWS Access Key ID provided.")

        # Get resource type from prefix
        prefix = aws_access_key_id[:4]
        resource_type = get_resource_type(prefix)

        # Decode AWS account ID
        account_id = aws_account_from_aws_key_id(aws_access_key_id)

        return {
            "statusCode": 200,
            "body": json.dumps({"account_id": account_id, "type": resource_type}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
        }

    except ValueError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": str(e)}),
            "headers": {"Content-Type": "application/json"},
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An internal error occurred."}),
            "headers": {"Content-Type": "application/json"},
        }


def get_aws_account_id(aws_access_key_id):
    """Return only the AWS account ID from an AWS access key ID."""
    try:
        if not aws_access_key_id or len(aws_access_key_id) < 4:
            raise ValueError("Invalid AWS Access Key ID provided.")
        return aws_account_from_aws_key_id(aws_access_key_id)
    except Exception as e:
        raise ValueError(f"Error extracting AWS account ID: {str(e)}")

