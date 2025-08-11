from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
PORT = int(os.getenv('PORT', 8001))
DEBUG = os.getenv('FLASK_ENV') == 'development'

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
    print("⚠️  WARNING: OPENAI_API_KEY not set or using default value")
    print("   Please create a .env file with your actual OpenAI API key")
    print("   Example: OPENAI_API_KEY=sk-your_actual_key_here")
    openai_available = False
else:
    try:
        openai.api_key = OPENAI_API_KEY
        # Test the API key with a simple request
        openai_available = True
        print(f"✅ OpenAI API key loaded successfully")
    except Exception as e:
        print(f"❌ OpenAI initialization error: {e}")
        openai_available = False

class ScriptGenerator:
    def __init__(self):
        self.training_data = []
        self.load_training_data()
    
    def load_training_data(self):
        """Load training data from scripts directory"""
        # Try multiple possible paths for scripts, prioritizing training folder
        possible_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'training'),
            os.path.join(os.path.dirname(__file__), '..', 'scripts'),
            os.path.join(os.path.dirname(__file__), 'scripts')
        ]
        
        for scripts_dir in possible_paths:
            if os.path.exists(scripts_dir):
                print(f"Loading training data from: {scripts_dir}")
                # Recursively search for .txt files in all subdirectories
                for root, dirs, files in os.walk(scripts_dir):
                    for filename in files:
                        if filename.endswith('.txt'):
                            filepath = os.path.join(root, filename)
                            try:
                                with open(filepath, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                    # Get relative path for better identification
                                    rel_path = os.path.relpath(filepath, scripts_dir)
                                    self.training_data.append({
                                        'filename': rel_path,
                                        'content': content
                                    })
                                    print(f"Loaded training data: {rel_path}")
                            except Exception as e:
                                print(f"Error loading {filename}: {e}")
                break
        
        print(f"Total training data loaded: {len(self.training_data)}")
    
    def parse_script_content(self, content):
        """Parse script content to extract training elements"""
        parsed = {
            'scenes': [],
            'characters': [],
            'dialogue': [],
            'descriptions': []
        }
        
        # Extract scenes (lines starting with INT./EXT.)
        scene_pattern = r'^(INT\.|EXT\.|INT\/EXT\.).*$'
        scenes = re.findall(scene_pattern, content, re.MULTILINE)
        parsed['scenes'] = scenes[:10]  # Limit to first 10 scenes
        
        # Extract character names (lines in ALL CAPS, usually dialogue)
        character_pattern = r'^[A-Z\s]+$'
        characters = re.findall(character_pattern, content, re.MULTILINE)
        parsed['characters'] = [c.strip() for c in characters if len(c.strip()) > 2][:20]
        
        # Extract dialogue (lines after character names)
        lines = content.split('\n')
        dialogue = []
        for i, line in enumerate(lines):
            if re.match(character_pattern, line.strip()) and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not re.match(character_pattern, next_line):
                    dialogue.append(f"{line.strip()}: {next_line}")
        parsed['dialogue'] = dialogue[:15]
        
        # Extract scene descriptions (lines between scenes and dialogue)
        descriptions = []
        for line in lines:
            line = line.strip()
            if (line and 
                not re.match(scene_pattern, line) and 
                not re.match(character_pattern, line) and
                not line.startswith('(') and
                not line.startswith('FADE') and
                len(line) > 20):
                descriptions.append(line)
        parsed['descriptions'] = descriptions[:10]
        
        return parsed
    
    def generate_script_scene_with_openai(self, prompt, context=None):
        """Generate a script scene using OpenAI API for intelligence + training data for content"""
        if not openai_available:
            return self.generate_script_scene_fallback(prompt, context)
        
        try:
            # Extract relevant content from training data based on prompt
            relevant_content = self._extract_relevant_training_content(prompt)
            
            # Create intelligent prompt for GPT to orchestrate the content
            system_prompt = f"""You are a professional screenwriter. Your job is to intelligently structure and combine content from training data to create compelling scenes.

Available Training Content:
{relevant_content}

Your Role:
- Use the training data above as your PRIMARY source of actual content
- Intelligently combine, adapt, and structure this content
- Maintain the style and tone of the training data
- Create coherent, engaging scenes
- Only generate new content if absolutely necessary to fill gaps

Instructions:
- Extract dialogue, descriptions, and action from training data
- Combine them intelligently based on the user's prompt
- Maintain screenplay format and structure
- Keep the authentic voice from the training data"""

            user_prompt = f"Create a compelling script scene about: {prompt}\n\nUse the training data above as your primary content source. Structure it intelligently into a complete scene."

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.3  # Lower temperature for more consistent use of training data
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self.generate_script_scene_fallback(prompt, context)
    
    def generate_movie_outline_with_openai(self, prompt, context=None):
        """Generate a movie outline using OpenAI API for intelligence + training data for content"""
        if not openai_available:
            return self.generate_movie_outline_fallback(prompt, context)
        
        try:
            # Extract relevant content from training data based on prompt
            relevant_content = self._extract_relevant_training_content(prompt)
            
            # Create intelligent prompt for GPT to orchestrate the content
            system_prompt = f"""You are a professional screenwriter. Your job is to intelligently structure and combine content from training data to create compelling movie outlines.

Available Training Content:
{relevant_content}

Your Role:
- Use the training data above as your PRIMARY source of actual content
- Intelligently combine, adapt, and structure this content into a 3-act outline
- Maintain the style and tone of the training data
- Create coherent, engaging plot structures
- Only generate new content if absolutely necessary to fill gaps

Instructions:
- Extract plot points, character arcs, themes, and scenes from training data
- Combine them intelligently based on the user's prompt
- Structure into a compelling 3-act outline
- Keep the authentic voice from the training data"""

            user_prompt = f"Create a compelling 3-act movie outline about: {prompt}\n\nUse the training data above as your primary content source. Structure it intelligently into a complete outline."

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=800,
                temperature=0.3  # Lower temperature for more consistent use of training data
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self.generate_movie_outline_fallback(prompt, context)
    
    def generate_script_scene_fallback(self, prompt, context=None):
        """Fallback script generation using training data as primary content source"""
        # Extract relevant content from training data
        relevant_content = self._extract_relevant_training_content(prompt)
        
        # Parse the training content to extract usable elements
        parsed_content = self._parse_training_content_for_fallback(relevant_content)
        
        # Create scene using training data
        scene_template = f"""FADE IN:

{parsed_content.get('scene_heading', 'INT. LOCATION - DAY')}

{parsed_content.get('scene_description', self._generate_scene_description(prompt))}

{parsed_content.get('character_name', 'CHARACTER NAME')}
{parsed_content.get('dialogue', self._generate_dialogue(prompt))}

{parsed_content.get('response_character', 'ANOTHER CHARACTER')}
{parsed_content.get('response_dialogue', self._generate_response(prompt))}

{parsed_content.get('action_line', self._generate_action_line(prompt))}

FADE OUT."""
        
        return scene_template
    
    def generate_movie_outline_fallback(self, prompt, context=None):
        """Fallback outline generation using training data as primary content source"""
        # Extract relevant content from training data
        relevant_content = self._extract_relevant_training_content(prompt)
        
        # Parse the training content to extract usable elements
        parsed_content = self._parse_training_content_for_fallback(relevant_content)
        
        # Create outline using training data
        outline_template = f"""MOVIE OUTLINE: {prompt[:50]}...

ACT I - SETUP
- Opening scene: {parsed_content.get('opening_scene', self._generate_scene_description(prompt))}
- Introduce main character: {parsed_content.get('character_intro', self._generate_character_description(prompt))}
- Inciting incident: {parsed_content.get('inciting_incident', self._generate_plot_point(prompt))}

ACT II - CONFRONTATION
- Rising action: {parsed_content.get('rising_action', self._generate_plot_point(prompt))}
- Midpoint: {parsed_content.get('midpoint', self._generate_plot_point(prompt))}
- Complications: {parsed_content.get('complications', self._generate_plot_point(prompt))}

ACT III - RESOLUTION
- Climax: {parsed_content.get('climax', self._generate_plot_point(prompt))}
- Falling action: {parsed_content.get('falling_action', self._generate_plot_point(prompt))}
- Resolution: {parsed_content.get('resolution', self._generate_plot_point(prompt))}

THEMES: {parsed_content.get('themes', self._generate_themes(prompt))}
GENRE: {parsed_content.get('genre', self._generate_genre(prompt))}"""
        
        return outline_template
    
    def _generate_scene_description(self, prompt):
        """Generate a scene description"""
        descriptions = [
            "A dimly lit room with shadows dancing on the walls",
            "A bustling city street filled with the sounds of life",
            "A quiet forest clearing where sunlight filters through leaves",
            "A modern office building with floor-to-ceiling windows",
            "A cozy coffee shop with the aroma of fresh brew"
        ]
        return descriptions[hash(prompt) % len(descriptions)]
    
    def _generate_dialogue(self, prompt):
        """Generate dialogue"""
        dialogue_options = [
            "I never thought it would come to this.",
            "Sometimes the hardest choices are the right ones.",
            "We all have our secrets, don't we?",
            "The past has a way of catching up with us.",
            "What if everything we know is wrong?"
        ]
        return dialogue_options[hash(prompt) % len(dialogue_options)]
    
    def _generate_response(self, prompt):
        """Generate a response line"""
        responses = [
            "You don't understand what's at stake.",
            "I wish it were that simple.",
            "Maybe we're asking the wrong questions.",
            "The truth is more complicated than that.",
            "Some things are better left unsaid."
        ]
        return responses[hash(prompt) % len(responses)]
    
    def _generate_action_line(self, prompt):
        """Generate an action line"""
        actions = [
            "Character looks out the window, lost in thought.",
            "A moment of silence hangs heavy in the air.",
            "Character paces back and forth, clearly agitated.",
            "The tension in the room is palpable.",
            "Character takes a deep breath, steeling themselves."
        ]
        return actions[hash(prompt) % len(actions)]
    
    def _generate_character_description(self, prompt):
        """Generate character description"""
        descriptions = [
            "A determined individual with a mysterious past",
            "Someone who has seen too much and learned too little",
            "A person caught between duty and desire",
            "An outsider looking for their place in the world",
            "A character with secrets that could change everything"
        ]
        return descriptions[hash(prompt) % len(descriptions)]
    
    def _generate_plot_point(self, prompt):
        """Generate a plot point"""
        plot_points = [
            "A discovery that changes everything",
            "A betrayal that shatters trust",
            "A choice that defines character",
            "A revelation that explains the past",
            "A decision that shapes the future"
        ]
        return plot_points[hash(prompt) % len(plot_points)]
    
    def _generate_themes(self, prompt):
        """Generate themes"""
        themes = [
            "Redemption and forgiveness",
            "Truth versus lies",
            "The price of ambition",
            "Love and sacrifice",
            "Identity and self-discovery"
        ]
        return themes[hash(prompt) % len(themes)]
    
    def _generate_genre(self, prompt):
        """Generate genre"""
        genres = [
            "Drama", "Thriller", "Romance", "Mystery", "Action"
        ]
        return genres[hash(prompt) % len(genres)]

    def _extract_relevant_training_content(self, prompt):
        """Extract the most relevant training content based on the prompt"""
        # Analyze prompt for keywords
        prompt_lower = prompt.lower()
        keywords = prompt_lower.split()
        
        # Score training data based on relevance
        scored_content = []
        for script in self.training_data:
            score = 0
            content_lower = script['content'].lower()
            
            # Score based on keyword matches
            for keyword in keywords:
                if keyword in content_lower:
                    score += 1
            
            # Score based on content length (more content = more options)
            score += len(script['content']) / 1000
            
            # Score based on filename relevance
            if any(keyword in script['filename'].lower() for keyword in keywords):
                score += 5
            
            scored_content.append((score, script))
        
        # Sort by relevance score and take top 3
        scored_content.sort(key=lambda x: x[0], reverse=True)
        top_content = scored_content[:3]
        
        # Format the content for GPT
        formatted_content = ""
        for score, script in top_content:
            formatted_content += f"\n--- Training Script: {script['filename']} (Relevance: {score:.1f}) ---\n"
            # Include more content since this is now the primary source
            formatted_content += script['content'][:1000] + "...\n"
        
        return formatted_content

    def _parse_training_content_for_fallback(self, training_content):
        """Parse training content to extract usable elements for fallback generation"""
        parsed = {}
        
        # Extract scene headings (INT./EXT.)
        scene_pattern = r'^(INT\.|EXT\.|INT\/EXT\.).*$'
        scenes = re.findall(scene_pattern, training_content, re.MULTILINE)
        if scenes:
            parsed['scene_heading'] = scenes[0]
        
        # Extract character names and dialogue
        character_pattern = r'^[A-Z\s]+$'
        lines = training_content.split('\n')
        dialogue_pairs = []
        
        for i, line in enumerate(lines):
            if re.match(character_pattern, line.strip()) and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not re.match(character_pattern, next_line):
                    dialogue_pairs.append((line.strip(), next_line))
        
        if dialogue_pairs:
            parsed['character_name'] = dialogue_pairs[0][0]
            parsed['dialogue'] = dialogue_pairs[0][1]
            if len(dialogue_pairs) > 1:
                parsed['response_character'] = dialogue_pairs[1][0]
                parsed['response_dialogue'] = dialogue_pairs[1][1]
        
        # Extract scene descriptions
        descriptions = []
        for line in lines:
            line = line.strip()
            if (line and 
                not re.match(scene_pattern, line) and 
                not re.match(character_pattern, line) and
                not line.startswith('(') and
                not line.startswith('FADE') and
                len(line) > 20):
                descriptions.append(line)
        
        if descriptions:
            parsed['scene_description'] = descriptions[0]
            parsed['opening_scene'] = descriptions[0]
        
        # Extract plot points and themes
        plot_points = [
            "A discovery that changes everything",
            "A betrayal that shatters trust", 
            "A choice that defines character",
            "A revelation that explains the past",
            "A decision that shapes the future"
        ]
        
        # Use training data if available, otherwise fallback
        if descriptions:
            parsed['inciting_incident'] = descriptions[1] if len(descriptions) > 1 else plot_points[0]
            parsed['rising_action'] = descriptions[2] if len(descriptions) > 2 else plot_points[1]
            parsed['midpoint'] = descriptions[3] if len(descriptions) > 3 else plot_points[2]
            parsed['complications'] = descriptions[4] if len(descriptions) > 4 else plot_points[3]
            parsed['climax'] = descriptions[5] if len(descriptions) > 5 else plot_points[4]
            parsed['falling_action'] = descriptions[6] if len(descriptions) > 6 else plot_points[0]
            parsed['resolution'] = descriptions[7] if len(descriptions) > 7 else plot_points[1]
        
        return parsed

# Initialize the script generator
script_generator = ScriptGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'training_data_count': len(script_generator.training_data),
        'openai_available': openai_available,
        'openai_status': 'configured' if openai_available else 'not_configured'
    })

@app.route('/generate', methods=['POST'])
def generate_script():
    """Generate script or outline based on prompt"""
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400
        
        prompt = data['prompt']
        output_type = data.get('outputType', 'script')
        conversation_history = data.get('conversationHistory', [])
        
        # Generate content based on output type
        if output_type == 'outline':
            content = script_generator.generate_movie_outline_with_openai(prompt, conversation_history)
        else:
            content = script_generator.generate_script_scene_with_openai(prompt, conversation_history)
        
        return jsonify({
            'content': content,
            'outputType': output_type,
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt
        })
        
    except Exception as e:
        app.logger.error(f"Error generating script: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/train', methods=['POST'])
def train_model():
    """Train the model with new script data"""
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({'error': 'Script content is required'}), 400
        
        script_id = data.get('scriptId')
        content = data['content']
        metadata = data.get('metadata', {})
        
        # Parse the script content
        parsed_data = script_generator.parse_script_content(content)
        
        # Add to training data
        training_item = {
            'id': script_id,
            'content': content,
            'metadata': metadata,
            'parsed': parsed_data,
            'timestamp': datetime.now().isoformat()
        }
        
        script_generator.training_data.append(training_item)
        
        # In a real implementation, you would:
        # 1. Fine-tune the model with the new data
        # 2. Update model weights
        # 3. Save the updated model
        
        return jsonify({
            'message': 'Training data processed successfully',
            'scriptId': script_id,
            'parsedData': parsed_data,
            'trainingDataCount': len(script_generator.training_data)
        })
        
    except Exception as e:
        app.logger.error(f"Error training model: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/scripts', methods=['GET'])
def get_training_scripts():
    """Get list of available training scripts"""
    try:
        scripts = []
        for item in script_generator.training_data:
            scripts.append({
                'id': item.get('id', 'unknown'),
                'filename': item.get('filename', 'unknown'),
                'metadata': item.get('metadata', {}),
                'parsed': item.get('parsed', {}),
                'timestamp': item.get('timestamp')
            })
        
        return jsonify({
            'scripts': scripts,
            'count': len(scripts)
        })
        
    except Exception as e:
        app.logger.error(f"Error getting scripts: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/scripts/<script_id>', methods=['GET'])
def get_training_script(script_id):
    """Get specific training script by ID"""
    try:
        for item in script_generator.training_data:
            if item.get('id') == script_id:
                return jsonify({
                    'script': item
                })
        
        return jsonify({'error': 'Script not found'}), 404
        
    except Exception as e:
        app.logger.error(f"Error getting script: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
