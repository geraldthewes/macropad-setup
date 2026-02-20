  Files created:                                                                                                                               
  - compile_macropad.py - Python compiler that converts YAML to shell script and cheat sheet                                                   
  - examples/current-emacs.yaml - Example YAML matching the current macropad.sh                                                                
  - examples/blank.yaml - Template for new configurations                                                                                      
  - requirements.txt - Python dependencies                                                                                                     

  Files modified:                                                                                                                              
  - Makefile - Added make compile target                                                                                                       
                                                                                                                                               
  Usage:                                                                                                                                       
  # Compile the YAML config
  make compile

  # Or run directly
  .venv/bin/python compile_macropad.py examples/current-emacs.yaml

  # Flash to macropad
  make install

  The generated macropad.sh matches the original configuration, and cheat-sheet.md provides human-readable documentation of all keys, macros,
  and encoders.


