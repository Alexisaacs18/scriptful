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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")

# Initialize OpenAI client
try:
    openai.api_key = OPENAI_API_KEY
    openai_available = True
except Exception as e:
    print(f"OpenAI initialization error: {e}")
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
        """Generate a script scene using OpenAI API"""
        if not openai_available:
            return self.generate_script_scene_fallback(prompt, context)
        
        try:
            # Create context from training data
            training_context = ""
            if self.training_data:
                # Use the first few training scripts as context
                context_scripts = self.training_data[:2]
                for script in context_scripts:
                    training_context += f"\n--- Training Script: {script['filename']} ---\n"
                    training_context += script['content'][:500] + "...\n"
            
            system_prompt = f"""You are a professional screenwriter. Generate a movie script scene based on the user's prompt.

Training Data Context:
{training_context}

Instructions:
- Write in proper screenplay format
- Include scene headings (INT./EXT.), character names in ALL CAPS, dialogue, and action descriptions
- Make it engaging and cinematic
- Keep the scene focused and well-paced
- Use the training data as inspiration for style and format"""

            user_prompt = f"Generate a movie script scene about: {prompt}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self.generate_script_scene_fallback(prompt, context)
    
    def generate_movie_outline_with_openai(self, prompt, context=None):
        """Generate a movie outline using OpenAI API"""
        if not openai_available:
            return self.generate_movie_outline_fallback(prompt, context)
        
        try:
            # Create context from training data
            context_scripts = self.training_data[:2]
            training_context = ""
            for script in context_scripts:
                training_context += f"\n--- Training Script: {script['filename']} ---\n"
                training_context += script['content'][:500] + "...\n"
            
            system_prompt = f"""You are a professional screenwriter. Generate a movie outline based on the user's prompt.

Training Data Context:
{training_context}

Instructions:
- Create a structured 3-act outline
- Include key plot points, character arcs, and themes
- Make it compelling and well-structured
- Use the training data as inspiration for style and content"""

            user_prompt = f"Generate a movie outline about: {prompt}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self.generate_movie_outline_fallback(prompt, context)
    
    def generate_script_scene_fallback(self, prompt, context=None):
        """Fallback script generation when OpenAI is not available"""
        # This is the original simplified generator
        scene_template = f"""FADE IN:

INT. LOCATION - DAY

{self._generate_scene_description(prompt)}

CHARACTER NAME
{self._generate_dialogue(prompt)}

ANOTHER CHARACTER
{self._generate_response(prompt)}

{self._generate_action_line(prompt)}

FADE OUT."""
        
        return scene_template
    
    def generate_movie_outline_fallback(self, prompt, context=None):
        """Fallback outline generation when OpenAI is not available"""
        outline_template = f"""MOVIE OUTLINE: {prompt[:50]}...

ACT I - SETUP
- Opening scene: {self._generate_scene_description(prompt)}
- Introduce main character: {self._generate_character_description(prompt)}
- Inciting incident: {self._generate_plot_point(prompt)}

ACT II - CONFRONTATION
- Rising action: {self._generate_plot_point(prompt)}
- Midpoint: {self._generate_plot_point(prompt)}
- Complications: {self._generate_plot_point(prompt)}

ACT III - RESOLUTION
- Climax: {self._generate_plot_point(prompt)}
- Falling action: {self._generate_plot_point(prompt)}
- Resolution: {self._generate_plot_point(prompt)}

THEMES: {self._generate_themes(prompt)}
GENRE: {self._generate_genre(prompt)}"""
        
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

# Initialize the script generator
script_generator = ScriptGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'training_data_count': len(script_generator.training_data)
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
