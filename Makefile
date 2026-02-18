DEVICE_ID := 5633

.PHONY: install print

install:
	bash macropad.sh

print:
	vitaly -i $(DEVICE_ID) layers -p
