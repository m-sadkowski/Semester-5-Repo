package lab.aui.app.domain.command;

import lombok.Builder;
import lombok.Data;

import java.util.UUID;

@Data
@Builder
public class CreateBrandCommand {
    private final UUID id;
    private final String name;
    private final String country;
}
