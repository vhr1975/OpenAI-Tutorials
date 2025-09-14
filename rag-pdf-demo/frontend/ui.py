"""
ui.py: Optional Streamlit or Chainlit UI for demo.
"""
# TODO: Implement simple UI for RAG PDF demo
import streamlit as st

def main():
	st.title("RAG PDF Demo")
	query = st.text_input("Enter your question:")
	if st.button("Submit"):
		# Stub: Call backend API or logic
		st.write("Answer: [stubbed answer]")

if __name__ == "__main__":
	main()
