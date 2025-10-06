from django.shortcuts import render
from .forms import PuzzleForm
import math
import random

# Define vowels for text puzzle
VOWELS = 'aeiouAEIOU'


def to_binary_8bit(text):
    """Convert text to 8-bit binary representation."""
    binary_result = []
    for char in text:
        # Get ASCII value and convert to 8-bit binary
        ascii_val = ord(char)
        binary_val = format(ascii_val, '08b')
        binary_result.append(f"{char}: {binary_val}")
    return binary_result


def simulate_treasure(limit_attempts=5):
    """Simulate a treasure hunt using binary search algorithm."""
    # Generate random secret number between 1 and 100
    secret = random.randint(1, 100)
    
    # Binary search simulation
    low = 1
    high = 100
    steps = []
    success = False
    
    for attempt in range(1, limit_attempts + 1):
        # Calculate middle point (binary search guess)
        guess = (low + high) // 2
        
        if guess == secret:
            steps.append({
                'attempt': attempt,
                'guess': guess,
                'result': 'Found the treasure!'
            })
            success = True
            break
        elif guess < secret:
            steps.append({
                'attempt': attempt,
                'guess': guess,
                'result': 'Too low'
            })
            low = guess + 1
        else:
            steps.append({
                'attempt': attempt,
                'guess': guess,
                'result': 'Too high'
            })
            high = guess - 1


    return {
        'secret': secret,
        'steps': steps,
        'attempts': len(steps),
        'success': success,
    }




def puzzle_view(request):
    context = {'form': PuzzleForm()}


    if request.method == 'POST':
        form = PuzzleForm(request.POST)
        context['form'] = form
        if form.is_valid():
            number = form.cleaned_data['number']
            text = form.cleaned_data['text']


            # Number puzzle
            is_even = (number % 2 == 0)
            sqrt_value = None
            cube_value = None
            note = None


            if is_even:
                if number >= 0:
                    sqrt_value = math.sqrt(number)
                else:
                    # real sqrt not defined for negative; show note
                    note = 'Square root not real for negative numbers.'
            else:
                cube_value = number ** 3


            # Text puzzle
            binary_text = to_binary_8bit(text)
            vowel_count = sum(1 for ch in text if ch in VOWELS)


            # Treasure hunt
            treasure = simulate_treasure(limit_attempts=5)


            context.update({
                'submitted': True,
                'number': number,
                'is_even': is_even,
                'sqrt_value': sqrt_value,
                'cube_value': cube_value,
                'note': note,
                'text': text,
                'binary_text': binary_text,
                'vowel_count': vowel_count,
                'treasure': treasure,
            })


    return render(request, 'puzzle/index.html', context)