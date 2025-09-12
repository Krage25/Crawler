def extract_video_content(content):
    try:
        # Split content into lines for better structure handling
        lines = content.split('\n')
        content_array = []
        
        # Flatten the content while preserving structure
        for line in lines:
            words = [word.strip() for word in line.split() if word.strip()]
            content_array.extend(words)
        
        # Print array for debugging
        print("CONTENT ARRAY:")
        for i, item in enumerate(content_array):
            print(f"{i}: {item}")
        
        found_content = False
        
        # Look for timestamp pattern (e.g., "0:08 / 1:49")
        for i in range(len(content_array)):
            current_word = content_array[i]
            
            # Check if the current word contains a timestamp pattern
            if "/" in current_word and ":" in current_word:
                parts = current_word.split('/')
                if len(parts) == 2 and ":" in parts[0] and ":" in parts[1]:
                    print(f"Found timestamp pattern at index {i}: {current_word}")
                    
                    # Extract content from after timestamp until "Like"
                    content_start = i + 1
                    content_end = None
                    
                    for j in range(content_start, len(content_array)):
                        if content_array[j] == "Like":
                            content_end = j
                            print(f"Found 'Like' at index {j}")
                            break
                    
                    if content_end:
                        extracted_words = content_array[content_start:content_end]
                        print(f"Extracted words: {extracted_words}")
                        
                        if extracted_words:
                            found_content = True
                            result = ' '.join(extracted_words)
                            print(f"FINAL RESULT: {result}")
                            return result
        
        # Alternative approach: Look for patterns like "1:49" followed by content
        if not found_content:
            print("Using alternative approach")
            for i in range(len(content_array)):
                current_word = content_array[i]
                
                # Check if word looks like a timestamp (e.g., "1:49")
                if ":" in current_word and all(part.isdigit() for part in current_word.split(":")):
                    print(f"Found timestamp at index {i}: {current_word}")
                    
                    # Content should start right after this
                    content_start = i + 3
                    content_end = None
                    
                    for j in range(content_start, len(content_array)):
                        if content_array[j] == "Like":
                            content_end = j
                            print(f"Found 'Like' at index {j}")
                            break
                    
                    if content_end:
                        extracted_words = content_array[content_start:content_end]
                        print(f"Extracted words: {extracted_words}")
                        
                        if extracted_words:
                            result = ' '.join(extracted_words)
                            print(f"FINAL RESULT: {result}")
                            return result
        
        return "Content not found"
    
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        traceback.print_exc()
        return "n/a"