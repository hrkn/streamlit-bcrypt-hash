import bcrypt
import streamlit


def main():
    streamlit.set_page_config(page_title="Bcrypt hash", layout="wide")
    streamlit.title("Bcrypt hash generator/validator")
    generator, validator = streamlit.columns(2)

    with generator:
        with streamlit.container(border=True):
            streamlit.header("Generate hash")
            streamlit.text(
                "Generate a bcrypt hash from your text. Higher rounds provide better security but take longer to process."
            )
            password = streamlit.text_input("Text to hash:")
            col_round, col_prefix = streamlit.columns([4, 1])
            with col_round:
                round = streamlit.slider(
                    "Rounds (Cost Factor):", min_value=1, max_value=17, value=12
                )
                match round:
                    case round if 1 <= round < 8:
                        streamlit.write(
                            ":red[Low security - not recommended for production]"
                        )
                    case round if 8 <= round < 12:
                        streamlit.write(":orange[Medium security - good for testing]")
                    case round if 12 <= round < 16:
                        streamlit.write(
                            ":green[High security - suitable for production]"
                        )
                    case round if 16 <= round:
                        streamlit.write(":blue[Excessive security - but very slow]")
            with col_prefix:
                prefix = streamlit.selectbox("Prefix:", ("2a", "2b"), index=1).encode()
            if streamlit.button(
                "Generate hash", disabled=(password == ""), width="stretch"
            ):
                hash = bcrypt.hashpw(
                    password.encode(), bcrypt.gensalt(round, prefix)
                ).decode()
                streamlit.code(hash, language="markdown")

    with validator:
        with streamlit.container(border=True):
            streamlit.header("Validate hash")
            streamlit.text("Check if a bcrypt hash matches the original text.")
            hash_to_verify = streamlit.text_input("Bcrypt hash:")
            original = streamlit.text_input("Original text:")
            if streamlit.button(
                "Verify hash",
                disabled=(hash_to_verify == "" or original == ""),
                width="stretch",
            ):
                if bcrypt.checkpw(original.encode(), hash_to_verify.encode()):
                    streamlit.success("✓ Hash matches the text")
                else:
                    streamlit.error("✗ Hash does not match the text")


if __name__ == "__main__":
    main()
